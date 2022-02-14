#!/bin/sh

##2e2mu
#sed -i 's~45.0323131973~42.46~g' *2e2mu*.txt
#sed -i 's~2.76577693912~3.33~g' *2e2mu*.txt
#sed -i 's~18.7073059~18.54~g' *2e2mu*.txt
#sed -i 's~rate 1.000 1.000 1.000~rate 0.96 0.96 0.96~g' *2e2mu*.txt

##4mu
#sed -i 's~38.0329665095~37.75~g' *4mu*.txt
#sed -i 's~3.85805764479~4.15~g' *4mu*.txt
#sed -i 's~17.2210039~16.88~g' *4mu*.txt

##4e
#sed -i 's~14.7674388388~13.91~g' *4e*.txt
#sed -i 's~1.70583143376~1.75~g' *4e*.txt
#sed -i 's~4.3786875~4.34~g' *4e*.txt
#sed -i 's~rate 1.000 1.000 1.000~rate 0.918 0.918 0.918~g' *4e*.txt


#sed -i 's~CMS_eff_e ~CMS_eff_e_2016 ~g' *.txt
#sed -i 's~CMS_eff_m ~CMS_eff_m_2016 ~g' *.txt
sed -i 's~CMS_hzz2e2mu_Zjets ~CMS_hzz2e2mu_Zjets_2016 ~g' *.txt
sed -i 's~CMS_hzz4e_Zjets ~CMS_hzz4e_Zjets_2016 ~g' *.txt
sed -i 's~CMS_hzz4mu_Zjets ~CMS_hzz4mu_Zjets_2016 ~g' *.txt
sed -i 's~CMS_zjets_bkgdcompo ~CMS_zjets_bkgdcompo_2016 ~g' *.txt
sed -i 's~lumi_13TeV ~lumi_13TeV_2016 ~g' *.txt
sed -i 's~CMS_zz4l_n_sig_1 ~CMS_zz4l_n_sig_1_2016 ~g' *.txt
sed -i 's~CMS_zz4l_n_sig_3 ~CMS_zz4l_n_sig_3_2016 ~g' *.txt
sed -i 's~CMS_zz4l_mean_m_sig ~CMS_zz4l_mean_m_sig_2016 ~g' *.txt
sed -i 's~CMS_zz4l_mean_e_sig ~CMS_zz4l_mean_e_sig_2016 ~g' *.txt
sed -i 's~CMS_zz4l_sigma_m_sig ~CMS_zz4l_sigma_m_sig_2016 ~g' *.txt
sed -i 's~CMS_zz4l_sigma_e_sig ~CMS_zz4l_sigma_e_sig_2016 ~g' *.txt
sed -i 's~CMS_zz4l_n_sig_2 ~CMS_zz4l_n_sig_2_2016 ~g' *.txt
