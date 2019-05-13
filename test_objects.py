import unittest
from objects import Entity, TowerTile, BaseTile, UnitTile


class TestObjects(unittest.TestCase):


    def test_Entity(self):
        ent1 = Entity()
        self.assertEqual(Entity.hm_entities(), 1)


    def test_BaseTile(self):
        tile_normal = BaseTile((0, 0))
        with self.assertRaises(ValueError):
            tile_negative1 = BaseTile((-1, 0))
            tile_negative2 = BaseTile((0, -1))
            tile_negative3 = BaseTile((-1, -1))
            tile_not_enough = BaseTile(0)


if __name__ == '__main__':
    unittest.main()





