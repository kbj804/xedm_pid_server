

'''import random

class Callmsg:
    
    def __init__(self):
        self.msg = "이 메세지는 __call__ 테스트 메세지 입니다. : "

    def printMsg(self, user_msg):
        um = self.msg + user_msg
        return um

    # 아래 함수를 클래스에 추가
    def __call__(self, user_msg):
        return self.printMsg(user_msg)

obj = Callmsg()
print(obj("Oh no"))

print(obj.msg)

class Memoize:
    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        print(self.memo)
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]

@Memoize
def fib(n):
    if n == 0 :
        return 0
    elif n == 1 :
        return 1
    else:
        return fib(n-1) + fib(n-2)
'''
# print(fib(40))

"""import asyncio

async def whoami_after_sleep(name, t):
  print(f'I am {name} and gonna sleep for {t} seconds.')
  await asyncio.sleep(t)
  print(f'I am {name}. I slept for {t} seconds.')
  return ('result', name, t)

async def main():
  await asyncio.gather(
    whoami_after_sleep('A', 1),
  )
  return "ok"

print(asyncio.run(main()))

# I am A and gonna sleep for 1 seconds.
# I am B and gonna sleep for 2 seconds.
# I am C and gonna sleep for 3 seconds.
# I am A. I slept for 1 seconds.
# I am B. I slept for 2 seconds.
# I am C. I slept for 3 seconds."""