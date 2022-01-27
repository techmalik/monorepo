#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

from copy import copy, deepcopy
from typing import Any, Dict, List, Optional, Set, Tuple
from mitosheet.state import State
from mitosheet.step_performers.step_performer import StepPerformer

class ChangeColumnFormatStepPerformer(StepPerformer):
    """"
    A change_column_format step, which allows you to change the format
    of a column(s)
    """
    @classmethod
    def step_version(cls) -> int:
        return 1

    @classmethod
    def step_type(cls) -> str:
        return 'change_column_format'

    @classmethod
    def step_display_name(cls) -> str:
        return 'Change Column Format'
    
    @classmethod
    def step_event_type(cls) -> str:
        return 'change_column_format_edit'

    @classmethod
    def saturate(cls, prev_state: State, params) -> Dict[str, str]:
        return params

    @classmethod
    def execute( # type: ignore
        cls,
        prev_state: State,
        sheet_index: int,
        column_ids: List[str],
        format_type: Dict[str, str],
        **params
    ) -> Tuple[State, Optional[Dict[str, Any]]]:

        # Make a post state, that is a deep copy
        post_state = copy(prev_state)

        # Actually update the format of the columns
        for column_id in column_ids:
            update_column_id_format(post_state, sheet_index, column_id, format_type)

        # Add the num_cols_formatted to the execution data for logging purposes. 
        return post_state, {'num_cols_formatted': len(column_ids)}

    @classmethod
    def transpile( # type: ignore
        cls,
        prev_state: State,
        post_state: State,
        execution_data: Optional[Dict[str, Any]],
        sheet_index: int,
        column_ids: List[str],
        format_type: Dict[str, str]
    ) -> List[str]:
        # Formatting columns only effects the display in Mito, not the generated code.
        return []
    
    @classmethod
    def describe( # type: ignore
        cls,
        sheet_index: int,
        column_ids: List[str],
        format_type: Dict[str,str],
        df_names=None,
        **params
    ) -> str:
        formated_column_ids = (', '.join(column_ids))
        return f'Formatted column{"s" if len(column_ids) > 1 else ""} {formated_column_ids} as {format_type["type"]}'

    @classmethod
    def get_modified_dataframe_indexes( # type: ignore
        cls, 
        sheet_index: int,
        column_ids: List[str],
        **params
    ) -> Set[int]:
        return {sheet_index}

def update_column_id_format(
    post_state: State,
    sheet_index: int,
    column_id: str,
    format_type: Dict[str, str]
) -> State: 
    post_state.column_format_types[sheet_index][column_id] = format_type
    return post_state


