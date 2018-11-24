class TextHistory:
    def __init__(self):
        self._text = ''
        self._version = 0
        self._history = [] #мы поставили подчеркивани, потому что не хотим чтобы эта переменная могла быть вызавна вне класса

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        raise AttributeError

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        raise AttributeError

    def check_version(self, from_version, to_version):
        if from_version is None or to_version is None or to_version <= from_version:
            raise ValueError

    def check_pos(self, pos=None):
        if pos is None:
            return len(self.text)
        if pos < 0 or pos >= len(self.text):
            raise ValueError('Недопустимое значение параметра pos')
        return pos

    def check_length(self, pos, length):
        if pos + length > len(self.text):
            raise ValueError('Недопустимое значение параметра length or pos')


    def insert(self, text, pos=None):
        pos = self.check_pos(pos)
        insert_action = InsertAction(pos=pos, text=text, from_version=self.version, to_version=self.version + 1)
        return self.action(insert_action)

    def replace(self, text, pos=None):
        pos = self.check_pos(pos)
        replace_action = ReplaceAction(pos=pos, text=text, from_version=self.version, to_version=self.version + 1)
        return self.action(replace_action)

    def delete(self, pos, length):
        pos = self.check_pos(pos)
        self.check_length(pos, length)
        delete_action = DeleteAction(pos=pos, length=length, from_version=self.version, to_version=self.version + 1)
        return self.action(delete_action)

    # def double(self):
    #     double_action = DoubleTextAction(pos=None, text=None, from_version=self.version, to_version=self.version + 1)
    #     return self.action(double_action)

    def action(self, action: 'Action'):
        self.check_version(action.from_version, action.to_version)
        new_text = action.apply(self.text)
        self._text = new_text
        self._version = action.to_version
        self._history.append(action)
        return self.version

    def get_actions(self, from_version=None, to_version=None):
        length_history = len(self._history)
        if from_version == to_version:
            return []
        if to_version is None:
            to_version = length_history
        if 0 <= from_version < to_version:
            if to_version <= length_history:
                return self._history[from_version:to_version]
            else:
                return self._history[from_version]
        raise ValueError


class Action:
    def __init__(self, pos, from_version, to_version, text=None, length=None):
        self.pos = pos
        self.from_version = from_version
        self.to_version = to_version
        self.text = text
        self.length = length

    def apply(self, text: str) -> str:
        raise NotImplementedError


class InsertAction(Action):
    def apply(self, text):
        if self.pos is None:
            return text + self.text

        return text[:self.pos] + self.text + text[self.pos:]


class ReplaceAction(Action):
    def apply(self, text):
        if self.pos is None:
            return text + self.text

        new_text = text[:self.pos] + self.text + text[self.pos + len(self.text):]
        return new_text


class DeleteAction(Action):
    def apply(self, text):

        new_text = text[:self.pos] + text[self.pos + self.length:]
        return new_text


# class DoubleTextAction(Action):
#     def apply(self, text: str):
#         return text * 2


if __name__ == '__main__':
    h = TextHistory()
    # # h.insert('abc')
    # h.double()
    # print(h.text)
