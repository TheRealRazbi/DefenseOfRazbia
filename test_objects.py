import unittest
from objects import Entity


class TestObjects(unittest.TestCase):


    def test_Entity(self):
        ent1 = Entity()
        self.assertEqual(Entity.hm_entities(), 1)


if __name__ == '__main__':
    unittest.main()





