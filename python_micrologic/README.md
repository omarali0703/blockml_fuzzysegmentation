# Python micro logic

> lets one create small scripts internally that can be run separately. These don't have to be stored here, but it keeps everything together you know?

## SLSeg parsing with the micro logic script
```bash
python3 micro_logic.py slseg '../dependencies/phd_datasets/slseg_outputs/gum/' True '../dependencies/phd_datasets/slseg_outputs/gum/binary'
```
## RS3 parsing with the micro logic script
> We need to use this code to parse the outputs of GUM. Whilst we have already done this, we may want more GUM data later so its good to have this here. This is also the wrong paths so we need to alter it.
```bash
python3 micro_logic.py rs3parse '../dependencies/phd_datasets/gum_outputs/original_gum_text/' True '../dependencies/phd_datasets/gum_outputs/original_gum_text_bin/'
```