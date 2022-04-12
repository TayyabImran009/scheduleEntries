if request.POST.get('Materialstage1') == "on":
	UpperArchMaterialBoxObj.stage1 = True
else:
	UpperArchMaterialBoxObj.stage1 = False
if request.POST.get('Materialstage2') == "on":
	UpperArchMaterialBoxObj.stage2 = True
else:
	UpperArchMaterialBoxObj.stage2 = False
if request.POST.get('Materialstage3') == "on":
	UpperArchMaterialBoxObj.stage3 = True
else:
	UpperArchMaterialBoxObj.stage3 = False
if request.POST.get('Materialstage4') == "on":
	UpperArchMaterialBoxObj.stage4 = True
else:
	UpperArchMaterialBoxObj.stage4 = False
if request.POST.get('Materialstage5') == "on":
	UpperArchMaterialBoxObj.stage5 = True
else:
	UpperArchMaterialBoxObj.stage5 = False
if request.POST.get('Materialstage6') == "on":
	UpperArchMaterialBoxObj.stage6 = True
else:
	UpperArchMaterialBoxObj.stage6 = False
if request.POST.get('Materialstage7') == "on":
	UpperArchMaterialBoxObj.stage7 = True
else:
	UpperArchMaterialBoxObj.stage7 = False
if request.POST.get('Materialstage8') == "on":
	UpperArchMaterialBoxObj.stage8 = True
else:
	UpperArchMaterialBoxObj.stage8 = False
if request.POST.get('Materialstage9') == "on":
	UpperArchMaterialBoxObj.stage9 = True
else:
	UpperArchMaterialBoxObj.stage9 = False
if request.POST.get('Materialstage10') == "on":
	UpperArchMaterialBoxObj.stage10 = True
else:
	UpperArchMaterialBoxObj.stage10 = False
if request.POST.get('Materialstage11') == "on":
	UpperArchMaterialBoxObj.stage11 = True
else:
	UpperArchMaterialBoxObj.stage11 = False
if request.POST.get('Materialstage12') == "on":
	UpperArchMaterialBoxObj.stage12 = True
else:
	UpperArchMaterialBoxObj.stage12 = False
if request.POST.get('Materialstage13') == "on":
	UpperArchMaterialBoxObj.stage13 = True
else:
	UpperArchMaterialBoxObj.stage13 = False
if request.POST.get('Materialstage14') == "on":
	UpperArchMaterialBoxObj.stage14 = True
else:
	UpperArchMaterialBoxObj.stage14 = False
if request.POST.get('Materialstage15') == "on":
	UpperArchMaterialBoxObj.stage15 = True
else:
	UpperArchMaterialBoxObj.stage15 = False
UpperArchMaterialBoxObj.save()