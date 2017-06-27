# gymgame

[gymgame](https://github.com/tornadoyi/gymgame) is game envrionment based on gym


## Quick Install

```bash
    # setup gymgame
    git clone https://github.com/tornadoyi/gymgame.git
    cd gymgame
    sudo python setup.py install
```


# Document

Run the game
```python
    import gym
	from gymgame.tinyrpg.man import config
	
	env = gym.make(config.GAME_NAME)
    env.reset()
	
	while True:
		if env.env.terminal: env.reset()
		env.step([])
		if render: env.render()
```



## Support

For any bugs or feature requests please:

File a new [issue](https://github.com/tornadoyi/gymgame/issues) or submit
a new [pull request](https://github.com/tornadoyi/gymgame/pulls) if you
have some code you'd like to contribute

For other questions and discussions please post a email to 390512308@qq.com


## License

We are releasing [gymgame](https://github.com/tornadoyi/gymgame) under an open source
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) License. We welcome you to contact us (390512308@qq.com) with your use cases.
