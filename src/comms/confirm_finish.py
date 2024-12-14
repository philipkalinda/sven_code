import sys
sys.path.insert(0, '../../../')
from sven.src.comms.slack_comms import SlackCommunicator

sc = SlackCommunicator()


if __name__=='__main__':

	sc.confirm_finish()
