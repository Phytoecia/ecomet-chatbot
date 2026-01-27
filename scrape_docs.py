import requests
from bs4 import BeautifulSoup
import time
import os

urls = [
  "https://phytoecia.github.io/eCOMET/articles/Interspecific_study_tutorial.html",
  "https://phytoecia.github.io/eCOMET/articles/Intro.html",
  "https://phytoecia.github.io/eCOMET/articles/Treatment-based_study_tutorial.html",
  "https://phytoecia.github.io/eCOMET/articles/eCOMET-intro.html",
  "https://phytoecia.github.io/eCOMET/articles/index.html",
  "https://phytoecia.github.io/eCOMET/articles/vignette-eCOMET-intro.html",
  "https://phytoecia.github.io/eCOMET/reference/AddChemDist.html",
  "https://phytoecia.github.io/eCOMET/reference/AddCustomAnnot.html",
  "https://phytoecia.github.io/eCOMET/reference/AddFeatureInfo.html",
  "https://phytoecia.github.io/eCOMET/reference/AddSiriusAnnot.html",
  "https://phytoecia.github.io/eCOMET/reference/AnovaBarPlot.html",
  "https://phytoecia.github.io/eCOMET/reference/BootCumulRichnessAUC.html",
  "https://phytoecia.github.io/eCOMET/reference/BootstrapCumulativeRichness.html",
  "https://phytoecia.github.io/eCOMET/reference/CalcNormalizedAUC.html",
  "https://phytoecia.github.io/eCOMET/reference/CalculateCumulativeRichness.html",
  "https://phytoecia.github.io/eCOMET/reference/CalculateGroupBetaDistance.html",
  "https://phytoecia.github.io/eCOMET/reference/CalculateNullCumulativeRichness.html",
  "https://phytoecia.github.io/eCOMET/reference/CanopusAllLevelEnrichmentPlot.html",
  "https://phytoecia.github.io/eCOMET/reference/CanopusLevelEnrichmentAnal.html",
  "https://phytoecia.github.io/eCOMET/reference/CanopusLevelEnrichmentPlot.html",
  "https://phytoecia.github.io/eCOMET/reference/CanopusListEnrichmentPlot.html",
  "https://phytoecia.github.io/eCOMET/reference/CanopusListEnrichmentPlot_2.html",
  "https://phytoecia.github.io/eCOMET/reference/ExportFeaturesToCSV.html",
  "https://phytoecia.github.io/eCOMET/reference/FeatureDendrogram.html",
  "https://phytoecia.github.io/eCOMET/reference/FeaturePerformanceRegression.html",
  "https://phytoecia.github.io/eCOMET/reference/FeaturePhenotypeCorrelation.html",
  "https://phytoecia.github.io/eCOMET/reference/FeaturePresence.html",
  "https://phytoecia.github.io/eCOMET/reference/FeatureToID.html",
  "https://phytoecia.github.io/eCOMET/reference/GenerateHeatmapInputs.html",
  "https://phytoecia.github.io/eCOMET/reference/GetAlphaDiversity.html",
  "https://phytoecia.github.io/eCOMET/reference/GetBetaDiversity.html",
  "https://phytoecia.github.io/eCOMET/reference/GetDAMs.html",
  "https://phytoecia.github.io/eCOMET/reference/GetDistanceMat.html",
  "https://phytoecia.github.io/eCOMET/reference/GetFunctionalHillNumber.html",
  "https://phytoecia.github.io/eCOMET/reference/GetGroupMeans.html",
  "https://phytoecia.github.io/eCOMET/reference/GetHillNumbers.html",
  "https://phytoecia.github.io/eCOMET/reference/GetLog2FoldChange.html",
  "https://phytoecia.github.io/eCOMET/reference/GetMZmineFeature.html",
  "https://phytoecia.github.io/eCOMET/reference/GetNormFeature.html",
  "https://phytoecia.github.io/eCOMET/reference/GetPerformanceFeatureCorrelation.html",
  "https://phytoecia.github.io/eCOMET/reference/GetPerformanceFeatureLMM.html",
  "https://phytoecia.github.io/eCOMET/reference/GetPerformanceFeatureRegression.html",
  "https://phytoecia.github.io/eCOMET/reference/GetRichness.html",
  "https://phytoecia.github.io/eCOMET/reference/GetSpecializationIndex.html",
  "https://phytoecia.github.io/eCOMET/reference/HCplot.html",
  "https://phytoecia.github.io/eCOMET/reference/IDToFeature.html",
  "https://phytoecia.github.io/eCOMET/reference/LoadMMO.html",
  "https://phytoecia.github.io/eCOMET/reference/LogNormalization.html",
  "https://phytoecia.github.io/eCOMET/reference/MSEA.html",
  "https://phytoecia.github.io/eCOMET/reference/MassNormalization.html",
  "https://phytoecia.github.io/eCOMET/reference/MeancenterNormalization.html",
  "https://phytoecia.github.io/eCOMET/reference/NMDSplot.html",
  "https://phytoecia.github.io/eCOMET/reference/PCAplot.html",
  "https://phytoecia.github.io/eCOMET/reference/PCoAplot.html",
  "https://phytoecia.github.io/eCOMET/reference/PLSDAplot.html",
  "https://phytoecia.github.io/eCOMET/reference/PairwiseComp.html",
  "https://phytoecia.github.io/eCOMET/reference/PlotFoldchangeResistanceQuad.html",
  "https://phytoecia.github.io/eCOMET/reference/PlotFoldchangeResistanceRegression.html",
  "https://phytoecia.github.io/eCOMET/reference/PlotFoldchangeResistanceRegression_t.html",
  "https://phytoecia.github.io/eCOMET/reference/PlotNPCStackedBar.html",
  "https://phytoecia.github.io/eCOMET/reference/ReorderGroups.html",
  "https://phytoecia.github.io/eCOMET/reference/ReplaceZero.html",
  "https://phytoecia.github.io/eCOMET/reference/SaveMMO.html",
  "https://phytoecia.github.io/eCOMET/reference/ScreenFeaturePhenotypeCorrelation.html",
  "https://phytoecia.github.io/eCOMET/reference/SwitchGroup.html",
  "https://phytoecia.github.io/eCOMET/reference/VolcanoPlot.html",
  "https://phytoecia.github.io/eCOMET/reference/ZNormalization.html",
  "https://phytoecia.github.io/eCOMET/reference/annotate_feature_info_ms2_from_mgf.html",
  "https://phytoecia.github.io/eCOMET/reference/anova_tukey_dunnett.html",
  "https://phytoecia.github.io/eCOMET/reference/ecomet-internal-imports.html",
  "https://phytoecia.github.io/eCOMET/reference/filter_canopus_annotations.html",
  "https://phytoecia.github.io/eCOMET/reference/filter_cosmic_structure.html",
  "https://phytoecia.github.io/eCOMET/reference/filter_mgf_to_mmo.html",
  "https://phytoecia.github.io/eCOMET/reference/filter_mmo.html",
  "https://phytoecia.github.io/eCOMET/reference/index.html",
  "https://phytoecia.github.io/eCOMET/reference/permanova_stat.html",
  "https://phytoecia.github.io/eCOMET/reference/print.mmo.html",
  "https://phytoecia.github.io/eCOMET/reference/write_anova.html"
]

output_file = "ecomet_reference_full.txt"

with open(output_file, "w") as f:
    f.write("# eCOMET Reference Documentation\n\n")

    for url in urls:
        print(f"Scraping {url}...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract Title
                title = soup.find('h1')
                title_text = title.text.strip() if title else url
                
                # Extract Usage/Signature (usually in <pre> or specific div)
                usage = ""
                usage_div = soup.find('div', class_='ref-usage') or soup.find('div', class_='sourceCode')
                if usage_div:
                    usage = usage_div.text.strip()
                
                # Extract Arguments (ref-arguments)
                args = ""
                args_div = soup.find('div', id='ref-arguments') or soup.find('div', class_='ref-arguments')
                if args_div:
                    args = args_div.text.strip()

                # Extract Description (ref-description)
                desc = ""
                desc_div = soup.find('div', class_='ref-description')
                if desc_div:
                    desc = desc_div.text.strip()
                
                # Extract Examples (ref-examples)
                examples = ""
                examples_div = soup.find('div', class_='ref-examples')
                if examples_div:
                    examples = examples_div.text.strip()
                
                # If article/tutorial, extract main content
                content = ""
                if "/articles/" in url:
                    main_content = soup.find('main')
                    if main_content:
                        content = main_content.text.strip()[:2000] # Limit content length
                
                f.write(f"\n## Function/Topic: {title_text}\n")
                f.write(f"URL: {url}\n")
                if desc: f.write(f"\n### Description\n{desc}\n")
                if usage: f.write(f"\n### Usage\n```r\n{usage}\n```\n")
                if args: f.write(f"\n### Arguments\n{args}\n")
                if examples: f.write(f"\n### Examples\n```r\n{examples}\n```\n")
                if content: f.write(f"\n### Article Content Summary\n{content}\n")
                
                f.write("\n" + "="*50 + "\n")
            else:
                print(f"Failed to fetch {url}: {response.status_code}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        # Be nice to the server
        time.sleep(0.5)

print(f"Scraping complete. Saved to {output_file}")
