from omegaconf import DictConfig, OmegaConf
from nemo.core.config import hydra_runner
from nemo.lightning import Trainer
from nemo.utils import logging
from nemo.utils.exp_manager import exp_manager
from nemo.utils.trainer_utils import resolve_trainer_cfg

import nemo.collections.asr as nemo_asr
import nemo.lightning as nl

@hydra_runner(config_path="configs", config_name="config")
def main(cfg: DictConfig) -> None:
    logging.info(OmegaConf.to_yaml(cfg, resolve=True))

    trainer = nl.Trainer(**resolve_trainer_cfg(cfg.trainer))
    exp_manager(trainer, cfg.get('exp_manager', None))
    model = nemo_asr.models.EncDecRNNTBPEModel(cfg=cfg.model, trainer=trainer)

    model.maybe_init_from_pretrained_checkpoint(cfg)

    trainer.fit(model)

    if hasattr(cfg.model, 'test_ds') and cfg.model.test_ds.manifest_filepath is not None:
        if model.prepare_data(trainer):
            trainer.test(model)

if __name__ == "__main__":
    main()
