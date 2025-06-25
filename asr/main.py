from nemo.core.config import hydra_runner
from omegaconf import DictConfig, OmegaConf

@hydra_runner(config_path="configs", config_name="config")
def main(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg, resolve=True))

if __name__ == "__main__":
    main()
