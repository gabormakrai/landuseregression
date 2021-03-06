from PIL import Image, ImageDraw
from PIL import ImageFont
import math
import matplotlib.pyplot as plt

gColors = []
for i in range(0, 255):
    gColors.append((255 - i, 255 - i, 255 - i))

colors = []
for i in range(0, 256):
    colors.append((i, 255, 0))
for i in range(0, 256):
    colors.append((255, 255 - i, 0))

def colorFromLevel(cLevel):
    if math.isnan(cLevel):
        return (255, 0, 0) # red
    
    index = int(round((cLevel - 0.0) / (200.0 - 0.0) * 256.0))
    if index >= 255:
        return gColors[254]
    else:
        return gColors[index] 

def colorFromLevel2(cLevel):
    if math.isnan(cLevel):
        return (0, 0, 255) # blue
    
    index = int(round((cLevel - 0.0) / (200.0 - 0.0) * 512.0))
    if index >= 511:
        return colors[511]
    else:
        return colors[index] 

def generateHeatmap(fileName, data, title, stationNames):
    
    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 20)
    fnt2 = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 30)
    
    im = Image.new('RGB', (1000, 1200), (255,255,255))
     
    draw = ImageDraw.Draw(im)
    
    draw.text((400,20), title, font=fnt2, fill=(0,0,0))
    
    for i in range(0, len(data)):
        draw.text((20,90 + i * 100), stationNames[i], font=fnt, fill=(0,0,0))
        
    for i in range(0, len(data)):
        for h in range(0, 168):
            draw.rectangle((210 + 3*h,70+i*100,210 + 3 * (h + 1),120+i*100),colorFromLevel(data[i][h]),None)
    
    # legend
    for i in range(0, 200):
        draw.rectangle((800,200 + 2 * i,850,200+2 * (i+1)),colorFromLevel(i),None)
        
    for i in range(0, 200):
        draw.rectangle((800,700 + 2 * i,850,700+2 * (i+1)),colorFromLevel(i),None)
        
    draw.rectangle((800,200,850,600), None, (128,128,128))
    draw.text((780,160), "obs/pred 0 ug/m3", font=fnt, fill=(0,0,0))
    draw.text((770,620), "200 ug/m3", font=fnt, fill=(0,0,0))
    draw.text((870,390), "100 ug/m3", font=fnt, fill=(0,0,0))
    
    draw.rectangle((800,700,850,1100), None, (128,128,128))
    draw.text((780,660), "error 0 ug/m3", font=fnt, fill=(0,0,0))
    draw.text((770,1120), "40 ug/m3", font=fnt, fill=(0,0,0))
    draw.text((870,890), "20 ug/m3", font=fnt, fill=(0,0,0))
    
    del draw
    
    im.save(fileName, "PNG")
    
def generateColorHeatmap(fileName, data, title, stationNames):
    
    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 20)
    fnt2 = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 30)
    
    im = Image.new('RGB', (1000, 1200), (255,255,255))
     
    draw = ImageDraw.Draw(im)
    
    draw.text((400,20), title, font=fnt2, fill=(0,0,0))
    
    for i in range(0, len(data)):
        draw.text((20,90 + i * 100), stationNames[i], font=fnt, fill=(0,0,0))

    for i in range(0, len(data)):
        for h in range(0, 168):
            draw.rectangle((210 + 3*h,70+i*100,210 + 3 * (h + 1),120+i*100),colorFromLevel2(data[i][h]),None)
                
    # legend
    for i in range(0, 200):
        draw.rectangle((800,200 + 2 * i,850,200+2 * (i+1)),colorFromLevel2(i),None)
        
    for i in range(0, 200):
        draw.rectangle((800,700 + 2 * i,850,700+2 * (i+1)),colorFromLevel2(i),None)
        
    draw.rectangle((800,200,850,600), None, (128,128,128))
    draw.text((780,160), "obs/pred 0 ug/m3", font=fnt, fill=(0,0,0))
    draw.text((770,620), "200 ug/m3", font=fnt, fill=(0,0,0))
    draw.text((870,390), "100 ug/m3", font=fnt, fill=(0,0,0))
    
    draw.rectangle((800,700,850,1100), None, (128,128,128))
    draw.text((780,660), "error 0 ug/m3", font=fnt, fill=(0,0,0))
    draw.text((770,1120), "40 ug/m3", font=fnt, fill=(0,0,0))
    draw.text((870,890), "20 ug/m3", font=fnt, fill=(0,0,0))
    
    
    del draw
    
    im.save(fileName, "PNG")    
    
def doLineChart(fileName, title, xAxis, yAxis, data, names):
            
    index = []
    for i in range(0, 168):
        index.append(i)
        
    fig = plt.figure(None, figsize=(10, 10))
    ax = fig.add_subplot(111)
    
    for i in range(0, len(data)):
        ax.plot(index, data[i], '-', label=names[i])
     
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(title)
    ax.legend()
         
    plt.margins(0.04, 0.04)
 
    plt.savefig(fileName)
    
def writeOutWeeklyData(filename, weeklyTimestamps, names, wData):
    output = open(filename, 'w')
    output.write("timestamp")
    for n in names:
        output.write(";" + n)
    output.write("\n")
    
    for i in range(0, len(weeklyTimestamps)):
        output.write(str(weeklyTimestamps[i]))
        for data in wData:
            output.write(";" + str(data[i]))
        output.write("\n")
        
    output.close()
    