#!/usr/bin/python3
#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import os

from matplotlib.font_manager import FontProperties
font=FontProperties(fname='/usr/share/fonts/adobe-source-han-sans/SourceHanSansCN-Normal.otf', size=10)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

def plot_from_dir(dir_path):
    files = os.listdir(dir_path)
    files = [ f for f in files if f.endswith('.txt') and (f.startswith('RA') or f.startswith('LD')) ]
    title = ''
    for filename in files:
        if filename.startswith('RA'):
            title = '随机接入配置下的RD曲线'
        else:
            title = '低延时配置下的RD曲线'
        performance_data= {}
        with open(filename, 'r') as file_content:
            lines = f.readlines()
            class_name = ''
            BitRateOrigin = []
            PsnrOrigin = []
            BitRateOpt = []
            PsnrOpt = []
            PointCount = 0
            get_class = False
            for line in lines:
                line = line.strip()
                if not len(line) or line.startswith('#') or line.startswith('lable'):
                    continue
                if not get_class:
                    if line.startswith('class') or line.startswith('Class') or line.startswith('CLASS'):
                        class_name = line[5] + '类序列'
                        get_class = True
                    continue
                value = [float(s) for s in line.split()]
                BitRateOrigin.append(value[0])
                PsnrOrigin.append(value[1])
                BitRateOpt.append(value[2])
                PsnrOpt.append(value[3])
                PointCount = PointCount + 1
                if PointCount == 4:
                    performance_data.update({class_name:[BitRateOrigin, PsnrOrigin, BitRateOpt, PsnrOpt]})
                    get_class = False
        print(performance_data)

def plot_figure(BitRateOrigin, PsnrOrigin, BitRateOpt, PsnrOpt, title, SavePath):
    fig = plt.figure()
    plt.subplots_adjust(left=0, right=1, top=0.9, bottom=0.1)
    plt.grid(ls='--')
    plt.xlabel("Bit rate(kbps)")
    plt.ylabel("PSNR(dB)")
    # Change label here
    plt.plot(BitRateOrigin, PsnrOrigin, color='red', label="HM16.15", marker='s')
    plt.plot(BitRateOpt, PsnrOpt, 'b--', label='Proposed', marker='^')
    plt.title(title)
    plt.legend(loc='lower right')
    plt.savefig(SavePath, dpi=500, bbox_inches='tight')

# get values from txt file
def plot_from_file(filename):
    mode = filename.split('.')[0]
    print("\n------------",mode,"------------\n")
    BitRateOrigin,PsnrOrigin = [], []
    BitRateOpt,PsnrOpt = [], []

    get_title = False
    PointCount = 0
    PlotCount = 0
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not len(line) or line.startswith('#'):
                continue
            if not get_title:
                if line.startswith("lable"):
                    title_line = [t for t in line.split(':', 1)]
                    if len(title_line) < 2:
                        print("lack of lable!")
                        continue
                    title = title_line[1].strip()
                    get_title = True
                continue
            value = [float(s) for s in line.split()]
            BitRateOrigin.append(value[0])
            PsnrOrigin.append(value[1])
            BitRateOpt.append(value[2])
            PsnrOpt.append(value[3])
            PointCount = PointCount + 1
            if PointCount==4:
                PlotCount = PlotCount+1
                print(PlotCount, title+"  plotting ...")

                # Change Save Path here
                if not os.path.exists('./'+mode):
                    os.makedirs('./'+mode)
                SavePath = './' + mode + '/' + title + '.png'
                SavePath = SavePath.replace(' ', '_')

                # Plot figure here
                plot_figure(BitRateOrigin, PsnrOrigin, BitRateOpt, PsnrOpt, title, SavePath)
                PointCount=0
                BitRateOrigin,PsnrOrigin = [], []
                BitRateOpt,PsnrOpt = [], []
                get_title = False

def main():
    p = argparse.ArgumentParser(description='plot figure from txt file')
    p.add_argument('data_file', help="Data file")
    flag=p.parse_args()
    filename = flag.data_file
    plot_from_file(filename)

if __name__ == "__main__":
    main()
