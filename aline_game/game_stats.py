import json

class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings=ai_game.settings
        self.reset_stats()
        #让游戏一开始处于非活动状态
        self.game_active=False
        # 从文件读取最高分
        try:
            with open("high_score.json", "r") as f:
                self.high_score = json.load(f)
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        """退出前保存最高分"""
        with open("high_score.json", "w") as f:
            json.dump(self.high_score, f)

    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.ships_left=self.settings.ship_limit
        self.score=0
        self.level=1
