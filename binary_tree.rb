require './tree_node.rb'
class BinaryTree
  attr_reader :root
  attr_writer :root

  def initialize(num)  
    @root = TreeNode.new(num) 
  end  
  
  def insert(num)  
    insert_recursive(num, @root)
  end  

  def insert_recursive(num, node)
    unless num == node.value
      if num > node.value
        if node.right_node.nil?
          node.set_right(TreeNode.new(num))
        else
          insert_recursive(num, node.right_node)
        end
      else
        if node.left_node.nil?
          node.set_left(TreeNode.new(num))
        else
          insert_recursive(num, node.left_node)
        end
      end
    end
  end

  def print_tree
    print_recursive(@root)
  end

  def print_recursive(node)
    unless node.nil?
      print_recursive(node.left_node)
      puts "Node value #{node.value}"
      print_recursive(node.right_node)
    end
  end

end

if __FILE__ == $0
  my_tree = BinaryTree.new(10)
  100.times do 
    my_tree.insert(Random.rand(100))
  end
  my_tree.print_tree
end
