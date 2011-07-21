#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import unittest

class Vector2:
	datatype = float
	
	def __init__(self, x=0.0, y=0.0):
		if isinstance(x, tuple):
			if y != 0.0:
				raise ValueError, 'If passing a tuple as first parameter, don\'t also pass a second number'
			
			# try to unpack 'x' as a tuple
			# allows us to convert a tuple to vector.
			
			if len(x) == 2: # xy
				self.x, self.y = x
		else:
			self.x = self.__class__.datatype(x)
			self.y = self.__class__.datatype(y)
		
		# since Vector2 is commonly used to describe resolution these aliases is used:
		self.width = self.x
		self.height = self.y
	
	def copy(self):
		return self.__class__(self.x, self.y)

	def xy(self):
		return (self.x, self.y)

	def __add__(self, rhs):
		return self.__class__(self.x + rhs.x, self.y + rhs.y)

	def __sub__(self, rhs):
		return self.__class__(self.x - rhs.x, self.y - rhs.y)
	
	def __mul__(self, rhs):
		try:
			# componentwise multiplication
			return self.__class__(self.x * rhs[0], self.y * rhs[1])
		except TypeError:
			# scalar multiplication
			return self.__class__(self.x * rhs, self.y * rhs)

	def __repr__(self):
		return '<vector (%.3f, %.3f)>' % (self.x, self.y)

	def length_squared(self):
		return self.x*self.x + self.y*self.y
	
	def length(self):
		return math.sqrt(self.length_squared())
	
	def normalize(self):
		len = self.length()
		return self.__class__(float(self.x) / len, float(self.y) / len)
	
	def ratio(self):
		return float(self.x) / float(self.y)

	def __iter__(self):
		return [self.x, self.y].__iter__()

	def __getitem__(self, index):
		return [self.x, self.y][index]

class Vector2f (Vector2):
	""" Alias for Vector2, just for consistency """
	pass

class Vector2i (Vector2):
	""" Vector2 with integer """
	datatype = int
	
	def __repr__(self):
		return '<vector (%d, %d)>' % (self.x, self.y)

class Vector3:
	def __init__(self, x=0.0, y=0.0, z=0.0):
		if isinstance(x, tuple):
			if y != 0.0 or z != 0.0:
				raise ValueError, 'If passing a tuple as first parameter, don\'t also pass a second or third number'
			
			# try to unpack 'x' as a tuple
			# allows us to convert a tuple to vector.
			
			if len(x) == 2: # xy
				self.x, self.y = x
				self.z = 0.0
			if len(x) == 3: # xyz
				self.x, self.y, self.z = x
		else:
			self.x = float(x)
			self.y = float(y)
			self.z = float(z)
	
	def copy(self):
		return self.__class__(self.x, self.y, self.z)

	def xyz(self):
		return (self.x, self.y, self.z)
	
	def xy(self):
		return (self.x, self.y)

	def __add__(self, rhs):
		return self.__class__(self.x + rhs.x, self.y + rhs.y, self.z+rhs.z)

	def __sub__(self, rhs):
		return self.__class__(self.x - rhs.x, self.y - rhs.y, self.z-rhs.z)
	
	# scalar multiplication
	def __mul__(self, scalar):
		return self.__class__(self.x * scalar, self.y * scalar, self.z * scalar)

	def __repr__(self):
		return '<vector (%.3f, %.3f, %.3f)>' % (self.x, self.y, self.z)

	def length_squared(self):
		return self.x*self.x + self.y*self.y + self.z*self.z
	
	def length(self):
		return math.sqrt(self.length_squared())
	
	def normalize(self):
		len = self.length()
		return self.__class__(self.x / len, self.y / len, self.z / len)

	def __iter__(self):
		return [self.x, self.y, self.z].__iter__()

	def __getitem__(self, index):
		return [self.x, self.y, self.z][index]

# ------------------------------------------------------------------------------
#
# Unittesting
#

if __name__ == '__main__':
	class test_vector2(unittest.TestCase):
		def test_constructor_empty(self):
			v = Vector2()
			self.assertEqual(v.x, 0.0)
			self.assertEqual(v.y, 0.0)
		
		def test_constructor_numbers(self):
			v = Vector2(1.0, 2.0)
			self.assertEqual(v.x, 1.0)
			self.assertEqual(v.y, 2.0)
		
		def test_constructor_tuple(self):
			v = Vector2((1.0, 2.0))
			self.assertEqual(v.x, 1.0)
			self.assertEqual(v.y, 2.0)
		
		def test_constructor_tuple_number(self):
			self.assertRaises(ValueError, Vector2, (1.0, 2.0), 3.0)
		
		def test_alias(self):
			v = Vector2(1.0, 2.0) * 2.0
			self.assertEqual(v.x, 2.0)
			self.assertEqual(v.y, 4.0)
			self.assertEqual(v.width, v.x)
			self.assertEqual(v.height, v.y)
			self.assertEqual(v[0], v.x)
			self.assertEqual(v[1], v.y)
			
		def test_copy(self):
			v1 = Vector2(1.0, 2.0)
			v2 = v1.copy()
			self.assertEqual(v2.x, 1.0)
			self.assertEqual(v2.y, 2.0)
			v1.x = 3.0
			v1.y = 4.0
			self.assertEqual(v2.x, 1.0)
			self.assertEqual(v2.y, 2.0)
			self.assertEqual(v1.x, 3.0)
			self.assertEqual(v1.y, 4.0)
		
		def test_swizzle(self):
			v = Vector2((1.0, 2.0))
			x,y = v.xy()
			self.assertEqual(x, 1.0)
			self.assertEqual(y, 2.0)
		
		def test_add(self):
			v1 = Vector2(1.0, 2.0)
			v2 = Vector2(3.0, 4.0)
			v3 = v1 + v2
			self.assertEqual(v3.x, 4.0)
			self.assertEqual(v3.y, 6.0)
		
		def test_sub(self):
			v1 = Vector2(1.0, 2.0)
			v2 = Vector2(3.0, 4.0)
			v3 = v1 - v2
			self.assertEqual(v3.x, -2.0)
			self.assertEqual(v3.y, -2.0)
		
		def test_mul_scalar(self):
			v1 = Vector2(1.0, 2.0)
			v2 = v1 * 2
			self.assertEqual(v2.x, 2.0)
			self.assertEqual(v2.y, 4.0)
		
		def test_lenght(self):
			v = Vector2(5.0, 5.0)
			self.assertAlmostEqual(v.length_squared(), 50.0)
			self.assertAlmostEqual(v.length(), 7.071, 3)
		
		def test_normalize(self):
			v1 = Vector2(5.0, 5.0)
			v2 = v1.normalize()
			self.assertAlmostEqual(v2.length_squared(), 1.0)
			self.assertAlmostEqual(v2.length(), 1.0)
		
		def test_ratio(self):
			v = Vector2(4.0, 3.0)
			self.assertAlmostEqual(v.ratio(), 1.33, 2)
		
		def test_iter(self):
			expected = [1.0, 2.0]
			v = Vector2(tuple(expected))
			for g,e in zip(v, expected):
				self.assertAlmostEqual(g,e)
	
	class test_vector3(unittest.TestCase):
		def test_constructor_empty(self):
			v = Vector3()
			self.assertEqual(v.x, 0.0)
			self.assertEqual(v.y, 0.0)
			self.assertEqual(v.z, 0.0)
		
		def test_constructor_numbers(self):
			v = Vector3(1.0, 2.0, 3.0)
			self.assertEqual(v.x, 1.0)
			self.assertEqual(v.y, 2.0)
			self.assertEqual(v.z, 3.0)
		
		def test_constructor_tuple2(self):
			v = Vector3((1.0, 2.0))
			self.assertEqual(v.x, 1.0)
			self.assertEqual(v.y, 2.0)
			self.assertEqual(v.z, 0.0)
		
		def test_constructor_tuple3(self):
			v = Vector3((1.0, 2.0, 3.0))
			self.assertEqual(v.x, 1.0)
			self.assertEqual(v.y, 2.0)
			self.assertEqual(v.z, 3.0)
		
		def test_constructor_tuple_number(self):
			self.assertRaises(ValueError, Vector3, (1.0, 2.0, 3.0), 4.0)
			self.assertRaises(ValueError, Vector3, (1.0, 2.0, 3.0), 4.0, 5.0)

		def test_alias(self):
			v = Vector3(1.0, 2.0, 3.0) * 2.0
			self.assertEqual(v.x, 2.0)
			self.assertEqual(v.y, 4.0)
			self.assertEqual(v.z, 6.0)
			self.assertEqual(v[0], v.x)
			self.assertEqual(v[1], v.y)
			self.assertEqual(v[2], v.z)
		
		def test_copy(self):
			v1 = Vector3(1.0, 2.0, 3.0)
			v2 = v1.copy()
			self.assertEqual(v2.x, 1.0)
			self.assertEqual(v2.y, 2.0)
			self.assertEqual(v2.z, 3.0)
			v1.x = 4.0
			v1.y = 5.0
			v1.z = 6.0
			self.assertEqual(v2.x, 1.0)
			self.assertEqual(v2.y, 2.0)
			self.assertEqual(v2.z, 3.0)
			self.assertEqual(v1.x, 4.0)
			self.assertEqual(v1.y, 5.0)
			self.assertEqual(v1.z, 6.0)
		
		def test_swizzle(self):
			v = Vector3((1.0, 2.0, 3.0))
			x,y = v.xy()
			self.assertEqual(x, 1.0)
			self.assertEqual(y, 2.0)
			x,y,z = v.xyz()
			self.assertEqual(x, 1.0)
			self.assertEqual(y, 2.0)
			self.assertEqual(z, 3.0)
		
		def test_add(self):
			v1 = Vector3(1.0, 2.0, 3.0)
			v2 = Vector3(4.0, 5.0, 6.0)
			v3 = v1 + v2
			self.assertEqual(v3.x, 5.0)
			self.assertEqual(v3.y, 7.0)
			self.assertEqual(v3.z, 9.0)
		
		def test_sub(self):
			v1 = Vector3(1.0, 2.0, 3.0)
			v2 = Vector3(4.0, 5.0, 6.0)
			v3 = v1 - v2
			self.assertEqual(v3.x, -3.0)
			self.assertEqual(v3.y, -3.0)
			self.assertEqual(v3.z, -3.0)
		
		def test_mul_scalar(self):
			v1 = Vector3(1.0, 2.0, 3.0)
			v2 = v1 * 2
			self.assertEqual(v2.x, 2.0)
			self.assertEqual(v2.y, 4.0)
			self.assertEqual(v2.z, 6.0)
		
		def test_lenght(self):
			v = Vector3(5.0, 5.0, 5.0)
			self.assertAlmostEqual(v.length_squared(), 75.0)
			self.assertAlmostEqual(v.length(), 8.660, 3)
		
		def test_normalize(self):
			v1 = Vector3(5.0, 5.0, 5.0)
			v2 = v1.normalize()
			self.assertAlmostEqual(v2.length_squared(), 1.0)
			self.assertAlmostEqual(v2.length(), 1.0)
		
		def test_iter(self):
			expected = [1.0, 2.0, 3.0]
			v = Vector3(tuple(expected))
			for g,e in zip(v, expected):
				self.assertAlmostEqual(g,e)
	
	class test_vector2_datatypes(unittest.TestCase):
		def test_int(self):
			v = Vector2i(1,2)
			self.assertEqual(type(v.x), int)
			self.assertEqual(type(v.y), int)
		
		def test_int_trunc(self):
			v = Vector2i(2.1, 2.9)
			self.assertEqual(v.x, 2)
			self.assertEqual(v.y, 2)
		
		def test_copy(self):
			v1 = Vector2i(1, 2)
			v2 = v1.copy()
			self.assertEqual(type(v1.x), int)
			self.assertEqual(type(v1.y), int)
			self.assertEqual(type(v2.x), int)
			self.assertEqual(type(v2.y), int)
			
			self.assertEqual(v2.x, 1)
			self.assertEqual(v2.y, 2)
			v1.x = 3
			v1.y = 4
			self.assertEqual(v2.x, 1)
			self.assertEqual(v2.y, 2)
			self.assertEqual(v1.x, 3)
			self.assertEqual(v1.y, 4)
			self.assertEqual(type(v1.x), int)
			self.assertEqual(type(v1.y), int)
			self.assertEqual(type(v2.x), int)
			self.assertEqual(type(v2.y), int)
	
	# I always miss this function, but there is probably a better way which I've
	# missed. I hope.
	def getTestsFromTestCases(self, names):
		cases = []
		for name in names:
			cases = cases + map(name, self.getTestCaseNames(name))
		return self.suiteClass(cases)
	unittest.TestLoader.getTestsFromTestCases = getTestsFromTestCases

	suite = unittest.TestLoader().getTestsFromTestCases([test_vector2, test_vector3, test_vector2_datatypes])
	unittest.TextTestRunner(verbosity=2).run(suite)

