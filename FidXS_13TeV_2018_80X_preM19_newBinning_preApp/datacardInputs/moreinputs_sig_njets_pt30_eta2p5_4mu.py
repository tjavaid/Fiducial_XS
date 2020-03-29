CB_mean = {} 
CB_sigma = {} 
folding = {'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0} 
dfolding = {'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin2': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin0_recobin4': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'ggH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ggH_NNLOPS_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'WH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin3': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin0': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin1': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin4_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin2': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin3': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin3_recobin4': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin3': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin2': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin1': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin0': -1.0, 'VBF_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin2_recobin4': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'ZH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin4': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin0': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin1': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin2': -1.0, 'ttH_powheg_JHUgen_125_4mu_njets_pt30_eta2p5_genbin1_recobin3': -1.0} 
