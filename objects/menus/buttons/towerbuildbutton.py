from objects.menus.buttons.buildmenubutton import BuildMenuButton, BuildMenu


class TowerBuildButton(BuildMenuButton):
    def __init__(self, screen, build_menu: BuildMenu, slot: int):
        super().__init__(screen, build_menu, slot)
        self.placing_tower = False

    def action(self):
        self.placing_tower = not self.placing_tower
