import gym

env = gym.make("Riverraid-ram-v0").env
for _ in range(10000):
    env.render()
    observation, reward, done, info = env.step(env.action_space.sample())

    if done:
        env.reset()
        print("Reset")

env.close()