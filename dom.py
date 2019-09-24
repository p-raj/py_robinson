# this package would be used to represent DOM for the HTML

class Node(object):
    def __init__(self, children, nodetype, nodeprops):
        self._nodetype = nodetype
        self._nodeprops = nodeprops
        # general representation of a Node children
        self.children = list()
        # data type for the Node
        #   nodetype = 'Text' or 'tag_name: div, p etc'
        #   nodeprops = {
        #   'tag_name' = String,
        #   'attributes' = {
        #           'text' = text
        #       }
        #   }
        self.nodetype = NodeType(nodetype, nodeprops)

    def __repr__(self):
        node = f'''
        NODE OBJECT:
            {self._nodetype}
            {self._nodeprops}
        '''
        return node

    def __str__(self):
        self.__repr__()


class NodeType(object):
    def __init__(self, nodetype, nodeprops):
        if nodetype == 'Text':
            self.node = Text(nodeprops)
        else:
            self.node = Element(nodeprops)

class Text(object):
    def __init__(self, nodeprops):
        # text is a string
        self.text = nodeprops.get('attributes').get('text', '')


class Element(object):
    def __init__(self, nodeprops):
        self.tag_name = nodeprops.get('tag_name')
        self.attributes = AttrMap(nodeprops.get('attributes'))


class AttrMap(object):
    def __init__(self, attributes):
        # attributes is a dict{}
        self.attrmap = attributes

# fn text(data: String) -> Node {
#     Node { children: Vec::new(), node_type: NodeType::Text(data) }
# }
def text(data):
    return Node(
        children=[],
        nodetype = 'Text',
        nodeprops = {
          'tag_name' : '',
          'attributes' : {
                'text' : data
            }
          }
    )

# fn elem(name: String, attrs: AttrMap, children: Vec<Node>) -> Node {
#     Node {
#         children: children,
#         node_type: NodeType::Element(ElementData {
#             tag_name: name,
#             attributes: attrs,
#         })
#     }
# }
def element(name, attributes, children):
    return Node(
        children=children,
        nodetype = 'Element',
        nodeprops = {
          'tag_name' : name,
          'attributes' : attributes
          }
    )
