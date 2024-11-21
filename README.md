# **适用于Unity的游戏内文本和对话的json编辑器**
**json Editor for in-game text and dialog with Unity Engine**

用于编辑特定格式的游戏内文本/对话的编辑器，支持插入和预览部分TextMeshPro支持的Rich Text Tags

## 支持格式

**默认编辑器** 

默认编辑器支持的json结构为
```
catalog:{
  item:{
    key:value
  }
}
```
，其中所有键和值均为`string`，如果值不为字符串，在读取并保存后会被转换为字符串形式保存。嵌套深度不足的json文件会导致程序崩溃，且不适合使用本编辑器编辑。


**对话编辑器** 

对话编辑器支持的格式比较复杂，详见[`test_files/NewDialog.json`](https://github.com/zdfjfd/jsonEditor/blob/dev/test_files/NewDialogs.json)。建议直接从主页新建对话，或者读取已有的对话文件进行修改。


## 特性

- 默认编辑器支持新建特定格式的json文件并进行编辑，修改和删除特定`catalog`，`item`或`key`。
- 对话编辑器支持复杂的游戏对话编辑，包括人物名称，对话所含选项，下一句对话id以及对话内容，同时也支持选项的编辑，包含选项的内容，选项的描述，选项的条件等。
- 对话编辑器同时支持对话的预览，在预览器处可以预览整个对话和选项的流程。
- 可以对加入的富文本标签进行预览，包括**加粗**，*斜体*，<u>下划线</u>，~~删除线~~和<span style="color: red;">文字颜色</span>，也可以手动输入还未支持的标签（[所有标签](https://docs.unity3d.com/Packages/com.unity.textmeshpro@4.0/manual/RichTextSupportedTags.html)），
  ，但是预览仅能显示HTML格式支持的标签。
- 支持插入自定义占位符，需要在placeholders.json文件中的`names`中添加对应的键和值，其中键可以以`{keyName}`形式插入至文本中，在预览模式下显示为对应的值。推荐使用默认编辑器对placeholders.json进行编辑，编辑完成后需要重启应用以生效。
- 支持自动保存，时间间隔在30秒至5分钟之间。
- 支持中文和英文。

