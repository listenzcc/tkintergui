# coding: utf-8

from components import Block


def build_blocks(root):
    blocks = {}

    '''
    # Column 1
    '''
    block = Block(root, name='Subject Info')
    block.place(
        relx=1/40, rely=1/40, relwidth=12/40, relheight=12/40, anchor='nw')
    blocks['subject_info'] = block

    block = Block(root, name='Connection Info')
    block.place(
        relx=1/40, rely=14/40, relwidth=12/40, relheight=11/40, anchor='nw')
    blocks['connection_info'] = block

    block = Block(root, name='Profile Info')
    block.place(
        relx=1/40, rely=26/40, relwidth=12/40, relheight=12/40, anchor='nw')
    blocks['profile_info'] = block

    '''
    # Column 2
    '''
    block = Block(root, name='Experiment I Info')
    block.place(
        relx=14/40, rely=1/40, relwidth=12/40, relheight=24/40, anchor='nw')
    blocks['experiment1_info'] = block

    block = Block(root, name='Model Training Info')
    block.place(
        relx=14/40, rely=26/40, relwidth=12/40, relheight=12/40, anchor='nw')
    blocks['modeltrain_info'] = block

    '''
    # Column 3
    '''
    block = Block(root, name='Experiment II Info')
    block.place(
        relx=27/40, rely=1/40, relwidth=12/40, relheight=37/40, anchor='nw')
    blocks['experiment2_info'] = block

    return blocks
