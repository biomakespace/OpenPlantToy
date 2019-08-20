
# Represents a single circuit connection
# Two circuit components joined
# to one another, including
# the directionality of the connection


class Connection:

    # Ordering of arguments, in hash
    # matches ordering sent
    # to controller by the components
    def __init__(self, downstream, upstream):
        self.downstream = downstream
        self.upstream = upstream

    def equals(self, compare):
        return self.upstream == compare.upstream and self.downstream == compare.downstream

    def hash(self):
        return self.downstream + self.upstream
