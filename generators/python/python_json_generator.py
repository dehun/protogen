from protogen.generators.basic_generator import BasicGenerator
from protogen.generators.template import CodeBlock

class PythonJsonGenerator(BasicGenerator):
    def generate(self, messages, outdir):
        # generate code blocks
        root = CodeBlock("root")
        root.add_block(CodeBlock("title", "#messages protocol"))
        _generate_messages(messages, root)
        _generate_factory(messages, root)
        # apply code blocks to template
        template = Template("./templates/root.pgt")
        code = template.generate(root)
        print code

    def _generate_messages(self, messages, root):
        messagesBlock = CodeBlock("messages")
        for msg in messages:
            self._generate_message(msg, messageBlock)
        root.add_block(messagesBlock)

    def _generate_message(self, msg, messagesBlock):
        template = Template("./templates/message.pgt")
        block = CodeBlock(msg.get_name())
        block.add_block(CodeBlock("name", msg.get_name()))
        self._generate_msg_members(msg, msgBlock)
        messagesBlock.add_block(CodeBlock(block.get_name(), template.generate(block)))

    def _generate_msg_members(self, msg, msgBlock):
        for paramBlock in [CodeBlock() for param in msg.__params__]
        pass
        
    def _generate_factory(self, messages, root):
        factoryBlock = CodeBlock("factory")
        root.add_block()


        
