import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlineInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption('Alice Invasion')
        #创建一个同于存储游戏统计信息的实例
        #并创建计分碑
        self.stats=GameStats(self)
        self.sb=Scoreboard(self)
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        #创建Play按钮
        self.play_button=Button(self,'Play')
        self.alien_bullets = pygame.sprite.Group()  # 新增子弹组


#下面定义了两个函数，用于简化run_game函数
    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()#退出保存
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pygame.K_ESCAPE:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建外星人群"""
        #创建一个外星人并计算一行容纳多少个外星人。
        #外星人的间距为外星人的宽度
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width - (2 * alien_width)
        number_aliens_x=available_space_x//(2 * alien_width)
        #计算屏幕可容纳多少行外星人。
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows=available_space_y//(2*alien_height)
        #创建一个外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self, alien_number,row_number):
        """创建一个外星人并将其放在当前行"""
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width+2*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #显示得分
        self.sb.show_score()
        #如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
        #外星人子弹
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        #更新子弹的位置
        self.bullets.update()
        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.start_new_level()  # 调用新方法

    def start_new_level(self):
        """开始新等级"""
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        # 在更新外星人时尝试射击
        for alien in self.aliens.sprites():
            alien.try_shoot(self)
        self.alien_bullets.update()  # 更新子弹位置
        # 使用像素级碰撞检测
        collision = pygame.sprite.spritecollideany(
            self.ship,
            self.aliens,
            collided=pygame.sprite.collide_mask  # 关键修改
        )
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #清理外星人子弹
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top > self.settings.screen_height:
                self.alien_bullets.remove(bullet)
        #确保子弹与飞船相撞
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_hit()
        #检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for aline in self.aliens.sprites():
            if aline.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个外星人下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left>0:
            #将ship_left减1并更新计分牌
            self.stats.ships_left-=1
            self.sb.prep_ships()
            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新外星人，并将飞船放到屏幕底部的中端
            self._create_fleet()
            self.ship.center_ship()
            #暂停
            sleep(1)
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                #像飞船被撞到一样处理
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        """统一游戏启动逻辑"""
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()  # 直接调用合并后的方法
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)


    #游戏主循环
    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai=AlineInvasion()
    ai.run_game()