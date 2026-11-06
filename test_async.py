import asyncio

async def taskA():
    print("Task A started")
    await asyncio.sleep(3)
    print("Task A finished")

async def taskB():
    print("Task B started")
    await asyncio.sleep(1)
    print("Task B finished")

async def taskC():
    print("Task C started")
    await asyncio.sleep(2)
    print("Task C finished")

async def main():
    coros = [taskA(), taskB(), taskC()]

    for finished_task in asyncio.as_completed(coros):
        result = await finished_task
        print(f"A task just completed!")

asyncio.run(main())

