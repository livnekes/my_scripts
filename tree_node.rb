class TreeNode
  attr_reader :left_node, :right_node, :value
  attr_writer :left_node, :right_node, :value

  def initialize(num)  
    @value = num 
    @left_node = nil
    @right_node = nil
  end  

  def set_left(node)
    @left_node = node
  end

  def set_right(node)
    @right_node = node
  end
  
end
