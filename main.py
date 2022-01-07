import sys


def dist_damerau_levenshteyn(lhs, rhs, distances=None):
    lhs_len = len(lhs)
    rhs_len = len(rhs)
    i_start = lhs_len - 1
    if i_start == -1:
        i_start = 0
    if distances is None:
        distances = {}
        for i in range(-1, lhs_len + 1):
            distances[(i, -1)] = i + 1
        for j in range(-1, rhs_len + 1):
            distances[(-1, j)] = j + 1
        i_start = 0
    else:
        distances[(lhs_len, -1)] = lhs_len + 1
    for i in range(i_start, lhs_len):
        for j in range(rhs_len):
            change_distance = distances[(i - 1, j - 1)]
            if lhs[i] != rhs[j]:
                change_distance += 1
            if i > 0 and j > 0 and lhs[i] == rhs[j - 1] and lhs[i - 1] == rhs[j]:
                distances[(i, j)] = min(distances[(i, j - 1)] + 1, distances[(i - 1, j)] + 1, change_distance,
                                        distances[(i - 2, j - 2)] + 1)
            else:
                distances[(i, j)] = min(distances[(i, j - 1)] + 1, distances[(i - 1, j)] + 1, change_distance)
    if lhs_len > rhs_len:
        lhs_sub_len = rhs_len
    else:
        lhs_sub_len = lhs_len
    return distances[lhs_len - 1, rhs_len - 1], distances[lhs_len - 1, lhs_sub_len - 1], distances


class vertex_:

    def __init__(self, key=None, parent=None, value=None, children=None):
        self.key = key
        self.value = value
        self.parent = parent
        if children is not None:
            self.children = self.children.append(children)
        else:
            self.children = []


class prefix_tree:
    def __init__(self):
        self.root = vertex_()

    def push(self, word):
        vertex = self.root
        word = word.lower()
        for i in range(len(word)):
            is_exist = False
            for child in vertex.children:
                if child.key == word[i]:
                    vertex = child
                    is_exist = True
                    break
            if not is_exist:
                for j in range(i, len(word), 1):
                    new_vertex = vertex_(word[j], vertex)
                    vertex.children.append(new_vertex)
                    vertex = new_vertex
                break
        vertex.value = word

    def search(self, word):
        word = word.lower()
        result = []
        black_vertexes = {}
        return_stack = []
        for child in self.root.children:
            return_stack.append(child)
        return_stack.reverse()
        vertex = self.root
        current_word = ''
        distances = {}
        for j in range(-1, len(word) + 1):
            distances[(-1, j)] = j + 1
        distances = None

        while True:
            full_distance, current_distance, distances = dist_damerau_levenshteyn(current_word, word, distances)
            if current_distance > 2:
                black_vertexes.update({vertex: True})
                if len(return_stack) == 0:
                    break
                vertex = return_stack.pop()
                current_word = current_word[:-1]
                continue
            if full_distance == 1 and vertex.value is not None:
                if result.count(vertex.value) == 0:
                    result.append(vertex.value)
            if full_distance == 0 and vertex.value is not None:
                return 1, []
            is_need_go_back = True
            for child in vertex.children:
                if black_vertexes.get(child):
                    continue
                return_stack.append(vertex)
                vertex = child
                current_word += vertex.key
                is_need_go_back = False
                break
            if not is_need_go_back:
                continue
            if len(return_stack) == 0:
                break
            black_vertexes.update({vertex: True})
            vertex = return_stack.pop()
            current_word = current_word[:-1]
        if len(result) == 0:
            return 2, []
        result.sort()
        return 3, result


if __name__ == '__main__':
    tree = prefix_tree()
    word_amount = int(sys.stdin.readline())
    for k in range(word_amount):
        line = sys.stdin.readline()
        if len(line) == 1:
            continue
        tree.push(line[:-1])
    for line in sys.stdin:
        if len(line) == 1:
            continue
        search_result = tree.search(line[:-1])
        if search_result[0] == 1:
            print(line[:-1], '-', 'ok')
            continue
        if search_result[0] == 2:
            print(line[:-1], '-?')
            continue
        if search_result[0] == 3:
            print(line[:-1], '->', end=' ')
            for m in range(len(search_result[1]) - 1):
                print(search_result[1][m], end=', ')
            print(search_result[1].pop())
