
# Represents a single circuit connection
# Two circuit components joined
# to one another, including
# the directionality of the connection


class Connection:

    def __init__(self, upstream, downstream):
        self.upstream = upstream
        self.downstream = downstream

    def equals(self, compare):
        return self.upstream == compare.upstream and self.downstream == compare.downstream
