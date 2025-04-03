class RaftNode:
    def __init__(self, node_id, peers):
        """
        Initializes a Raft node with the given node ID and list of peers.

        Args:
            node_id (int): The unique identifier of the node.
            peers (list): A list of the other nodes in the cluster.
        """
        self.node_id = node_id
        self.peers = peers
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        self.next_index = {peer: 0 for peer in peers}
        self.match_index = {peer: 0 for peer in peers}
        self.state = 'follower'

    def request_vote(self, candidate_id, last_log_index, last_log_term):
        """
        Sends a vote request to the other nodes in the cluster.

        Args:
            candidate_id (int): The ID of the candidate requesting the vote.
            last_log_index (int): The index of the candidate's last log entry.
            last_log_term (int): The term of the candidate's last log entry.
        """
        # Send vote request to peers
        pass

    def append_entries(self, leader_id, prev_log_index, prev_log_term, entries, leader_commit):
        """
        Sends log entries to the other nodes in the cluster.

        Args:
            leader_id (int): The ID of the leader sending the entries.
            prev_log_index (int): The index of the log entry immediately preceding the new ones.
            prev_log_term (int): The term of the log entry immediately preceding the new ones.
            entries (list): The new log entries to append.
            leader_commit (int): The leader's commit index.
        """
        # Send log entries to peers
        pass

    def handle_message(self, message):
        """
        Handles incoming messages from other nodes in the cluster.

        Args:
            message (dict): The message to handle.
        """
        if message['type'] == 'vote_request':
            # Handle vote request
            pass
        elif message['type'] == 'vote_response':
            # Handle vote response
            pass
        elif message['type'] == 'append_entries':
            # Handle log entries
            pass
        elif message['type'] == 'append_entries_response':
            # Handle log entries response
            pass

    def run(self):
        """
        The main loop of the Raft node. Handles messages and state transitions based on the current state of the node.
        """
        while True:
            if self.state == 'follower':
                # Handle messages from leader or candidate
                pass
            elif self.state == 'candidate':
                # Request votes from peers
                pass
            elif self.state == 'leader':
                # Send log entries to peers
                pass

    class RequestVoteArgs:
        """
        The format of a vote request message.
        """
        def __init__(self, term, candidate_id, last_log_index, last_log_term):
            self.term = term
            self.candidate_id = candidate_id
            self.last_log_index = last_log_index
            self.last_log_term = last_log_term

    class RequestVoteReply:
        """
        The format of a vote response message.
        """
        def __init__(self, term, vote_granted):
            self.term = term
            self.vote_granted = vote_granted

    class AppendEntriesArgs:
        """
        The format of a log entry message.
        """
        def __init__(self, term, leader_id, prev_log_index, prev_log_term, entries, leader_commit):
            self.term = term
            self.leader_id = leader_id
            self.prev_log_index = prev_log_index
            self.prev_log_term = prev_log_term
            self.entries = entries
            self.leader_commit = leader_commit

    class AppendEntriesReply:
        """
        The format of a log entry response message.
        """
        def __init__(self, term, success):
            self.term = term
            self.success = success

    class LogEntry:
        """
        The format of a log entry.
        """
        def __init__(self, term, command):
            self.term = term
            self.command = command