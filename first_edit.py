class FirstEdit(achievements.Achievement):
    def __init__(self):
        super(FirstEdit, self).__init__(self.check, "Your First Edit", "static/first_acc.png")


    def check(self, curr, user):
        curr.execute('SELECT count(1) FROM edits WHERE username=%(u)s', {'u':user})
        row = curr.fetchone()
        return row[0] == 1
