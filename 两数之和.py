def func(nums: list[int], target: int) -> list[int]:
    '''暴力破解法'''
    result = []
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
              if nums[i] + nums[j] == target:
                result.append(i)
                result.append(j)
                return result
    return result

if __name__  == '__main__':
    nums = [11, 15, 2, 7]
    target = 9
    print(func(nums, target))

class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        '''哈希表法'''
        seen = {}
        for i, num in enumerate(nums):
            diff = target - num
            if diff in seen:
                return [seen[diff], i]
            seen[num] = i
        return []

if __name__ == '__main__':
    nums = [11, 15, 2, 7]
    target = 9
    print(Solution().twoSum(nums, target))
    