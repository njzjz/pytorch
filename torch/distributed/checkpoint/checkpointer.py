from typing import Optional, Dict, Any

import torch.distributed as dist
from torch.distributed.checkpoint.metadata import STATE_DICT_TYPE
from torch.distributed.checkpoint.storage import SavePlanner, LoadPlanner
from torch.distributed.checkpoint.storage import StorageReader, StorageWriter
import torch.distributed.checkpoint.state_dict_saver as saver
import torch.distributed.checkpoint.state_dict_loader as loader

__all__ = ["Checkpointer"]

class Checkpointer:

    def __init__(
        self,
        storage_writer: StorageReader,
        storage_reader: StorageWriter,
        process_group: Optional[dist.ProcessGroup] = None,
        coordinator_rank: int = 0,
        no_dist: bool = False,
        planner: Optional[LoadPlanner] = None,
    ):
        self.storage_writer = storage_writer
        self.storage_reader = storage_reader
        self.process_group = process_group
        self.coordinator_rank = coordinator_rank
        self.no_dist = no_dist
        self.planner = planner

    def save(
        self,
        state_dict: STATE_DICT_TYPE,
        *,
        storage_writer: Optional[StorageWriter] = None,
        process_group: Optional[dist.ProcessGroup] = None,
        coordinator_rank: int = 0,
        no_dist: bool = False,
        planner: Optional[SavePlanner] = None,
    ):
        storage_writer = storage_writer or self.storage_writer
        process_group = process_group or self.process_group
        coordinator_rank = coordinator_rank or self.coordinator_rank
        no_dist = no_dist or self.no_dist
        planner = planner or self.planner

        saver.save(
            state_dict,
            storage_writer,
            process_group,
            coordinator_rank,
            no_dist,
            planner
        )

    def load(
            self,
            state_dict: Dict[str, Any],
            *,
            storage_reader: Optional[StorageReader] = None,
            process_group: Optional[dist.ProcessGroup] = None,
            coordinator_rank: int = 0,
            no_dist: bool = False,
            planner: Optional[LoadPlanner] = None,
    ):
        storage_reader = storage_reader or self.storage_reader
        process_group = process_group or self.process_group
        coordinator_rank = coordinator_rank or self.coordinator_rank
        no_dist = no_dist or self.no_dist
        planner = planner or self.planner

        loader.load(
            state_dict,
            storage_reader,
            process_group,
            coordinator_rank,
            no_dist,
            planner
        )
