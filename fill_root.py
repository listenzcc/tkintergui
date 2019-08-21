# coding: utf-8

from components import Block


def build_blocks(root):

    blocks = {}

    bg = '#f0f0f0'
    bg = None

    ########################
    # Column 1
    # Subject Info
    block = Block(root, name='被试信息', bg=bg)
    block.place(
        relx=1/40, rely=6/40, relwidth=12/40, relheight=10/40, anchor='nw')
    blocks['subject_info'] = block
    # Connection Info
    block = Block(root, name='连接信息', bg=bg)
    block.place(
        relx=1/40, rely=17/40, relwidth=12/40, relheight=10/40, anchor='nw')
    blocks['connection_info'] = block
    # Profile Info
    block = Block(root, name='保存设置', bg=bg)
    block.place(
        relx=1/40, rely=28/40, relwidth=12/40, relheight=10/40, anchor='nw')
    blocks['profile_info'] = block

    ########################
    # Column 2
    # Experiment I Info
    block = Block(root, name='训练实验阶段', bg=bg)
    block.place(
        relx=14/40, rely=6/40, relwidth=12/40, relheight=15/40, anchor='nw')
    blocks['experiment1_info'] = block
    # Model Training Info
    block = Block(root, name='训练模型信息', bg=bg)
    block.place(
        relx=14/40, rely=23/40, relwidth=12/40, relheight=15/40, anchor='nw')
    blocks['modeltrain_info'] = block

    ########################
    # Column 3
    # Experiment II Info
    block = Block(root, name='测试实验阶段', bg=bg)
    block.place(
        relx=27/40, rely=6/40, relwidth=12/40, relheight=32/40, anchor='nw')
    blocks['experiment2_info'] = block

    return blocks
