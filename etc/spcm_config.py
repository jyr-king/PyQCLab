# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 17:37:29 2018

@author: jyr_king
"""

spcm_rep_run_modes={
                'cont':SPC_REP_STD_CONTINUOUS,
                'single':SPC_REP_STD_SINGLE,
                'multi':SPC_REP_STD_MULTI,
                'gate':SPC_REP_STD_GATE,
                'sequence':SPC_REP_STD_SEQUENCE,
                'single_r':SPC_REP_STD_SINGLERESTART,
                'single_fifo':SPC_REP_FIFO_SINGLE,
                'multi_fifo':SPC_REP_FIFO_MULTI,
                'gate_fifo':SPC_REP_FIFO_GATE
                }
spcm_daq_run_modes={
                'std_single':SPC_REC_STD_SINGLE,
                'std_multi':SPC_REC_STD_MULTI,
                'std_gate':SPC_REC_STD_GATE,
                'std_aba':SPC_REC_STD_ABA,
                'std_segstats':SPC_REC_STD_SEGSTATS,
                'std_average':SPC_REC_STD_AVERAGE,
                'fifo_single':SPC_REC_FIFO_SINGLE,
                'fifo_multi':SPC_REC_FIFO_MULTI,
                'fifo_gate':SPC_REC_FIFO_GATE,
                'fifo_aba':SPC_REC_FIFO_ABA,
                'fifo_segstats':SPC_REC_FIFO_SEGSTATS,
                'fifo_average':SPC_REC_FIFO_AVERAGE
                }
spcm_clock_modes={
                'int':SPC_CM_INTPLL,
                'ext':SPC_CM_EXTREFCLOCK
                }
spcm_trig_sources={
            'sw':SPC_TMASK_SOFTWARE,
            'ext0':SPC_TMASK_EXT0,
            'ext1':SPC_TMASK_EXT1,
            'ext01':SPC_TMASK_EXT0 | SPC_TMASK_EXT1
            }
spcm_trig_masks={
            'or':SPC_TRIG_ORMASK,
            'and':SPC_TRIG_ANDMASK
            }
spcm_trig_modes={
            'pos':SPC_TM_POS,
            'neg':SPC_TM_NEG,
            'both':SPC_TM_BOTH,
            'winenter':SPC_TM_WINENTER,
            'winleave':SPC_TM_WINLEAVE,
            'inwin':SPC_TM_INWIN,
            'outwin':SPC_TM_OUTSIDEWIN
            }