class Character:
    def __init__(self, job: str, src: str, lv: str, name: str):
        self.__job = job
        self.__src = src
        self.__lv = lv
        self.__name = name
        self.__item_lv = None

    def __str__(self):
        return " ".join([self.name, self.job, self.lv])

    def add_item_lv(self, lv):
        self.__item_lv = lv

    # 직업
    @property
    def job(self):
        return self.__job

    # 직업 이미지 링크
    @property
    def src(self):
        return self.__src

    # 전투 레벨
    @property
    def lv(self):
        return self.__lv

    # 이름
    @property
    def name(self):
        return self.__name

    # 아이템 최대 레벨
    @property
    def item_lv(self):
        return self.__item_lv
