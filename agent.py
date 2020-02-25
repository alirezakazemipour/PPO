from model import Model
from torch.optim import Adam
from torch import from_numpy
from torch.distributions import Categorical
from torch.nn import MSELoss


class Agent:
    def __init__(self, state_shape, n_actions, lr):
        self.n_actions = n_actions
        self.state_shape = state_shape
        self.lr = lr
        self.new_policy = Model(state_shape=self.state_shape, n_actions=self.n_actions)
        self.old_policy = Model(state_shape=self.state_shape, n_actions=self.n_actions)

        self.old_policy.load_state_dict(self.new_policy.state_dict())

        self.optimizer = Adam(self.new_policy.parameters(), lr=self.lr)
        self.critic_loss = MSELoss()

    def choose_action(self, state):
        state = from_numpy(state).float()
        v, pi = self.new_policy(state)
        action = Categorical(pi).sample().cpu()

        return action, v

    def optimize(self, loss):

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def set_weights(self):
        for old_params, new_params in zip(self.old_policy.parameters(), self.new_policy.parameters()):
            old_params.data.copy_(new_params.data)