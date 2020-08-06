from app import db, bcrypt
from flask import jsonify, abort, redirect, url_for, make_response
from app.models import *
import json
import jsonpickle
from json import JSONEncoder
from datetime import datetime, date

# Provide Generic Success #
###########################
def provideGenericSuccess():
    return jsonify({'response': 'success'})

# Get List of Product Families #
################################
def getProductFamilies():
    arrProdFamilies = []
    models = MODEL.query.filter_by(isActive=True).all()

    for model in models:
        if model.family not in arrProdFamilies:
            arrProdFamilies.append(model.family)

    return arrProdFamilies

# Get List of Product Models   #
################################
def getProductModels(family):
    arrModels = []
    models = MODEL.query.filter_by(family=family, isActive=True).all()

    for model in models:
            child = {}
            child['varName']  = model.varName
            child['label']    = model.label
            child['family']   = model.family
            child['attrSet']  = model.attrSet
            child['isActive'] = model.isActive
            arrModels.append(child)

    arrRet = {'Models':arrModels}
    return arrRet

# Get List of Attribute Definitions #
#####################################
def getAttributeDefinitions(model):
    model = MODEL.query.filter_by(varName=model).first()
    attrSet = ATTRSET.query.filter_by(id=model.attrSet).first()

    retDict = {}
    retDict['id']  = attrSet.id
    retDict['attr1Label']  = attrSet.attr1Label
    retDict['attr2Label']  = attrSet.attr2Label
    retDict['attr3Label']  = attrSet.attr3Label
    retDict['attr4Label']  = attrSet.attr4Label
    retDict['attr5Label']  = attrSet.attr5Label
    retDict['attr1LOV']  = attrSet.attr1LOV
    retDict['attr2LOV']  = attrSet.attr2LOV
    retDict['attr3LOV']  = attrSet.attr3LOV
    retDict['attr4LOV']  = attrSet.attr4LOV
    retDict['attr5LOV']  = attrSet.attr5LOV

    arrRet = {'attributeSet':retDict}
    return arrRet

# Query parts based on attributes #
###################################
def queryPartsByAttribute(model, attr1, attr2, attr3, attr4, attr5):
    #model   = MODEL.query.filter_by(varName=model).first()
    #attrSet = ATTRSET.query.filter_by(id=model.attrSet).first()
    arrParts = []
    parts   = PRODUCT.query.filter_by(
                productModel=model, 
                attrVal1=attr1, 
                attrVal2=attr2,
                attrVal3=attr3,
                attrVal4=attr4,
                attrVal5=attr5,
                isActive=True
            ).all()

    for part in parts:
        child = {}
        child['partNum']      = part.partNum
        child['description']  = part.description
        child['isActive']     = part.isActive
        child['listNRC']      = part.listNRC
        child['listMRC']      = part.listMRC
        child['productModel'] = part.productModel
        child['attrVal1']     = part.attrVal1
        child['attrVal2']     = part.attrVal2
        child['attrVal3']     = part.attrVal3
        child['attrVal4']     = part.attrVal4
        child['attrVal5']     = part.attrVal5
        arrParts.append(child)

    arrRet = {'Parts':arrParts}
    return arrRet

# Query parts based on model only #
###################################
def queryPartsByModel(model):
    #model   = MODEL.query.filter_by(varName=model).first()
    #attrSet = ATTRSET.query.filter_by(id=model.attrSet).first()
    arrParts = []
    parts   = PRODUCT.query.filter_by(
                productModel=model,
                isActive=True
            ).all()

    for part in parts:
        child = {}
        child['partNum']      = part.partNum
        child['description']  = part.description
        child['isActive']     = part.isActive
        child['listNRC']      = part.listNRC
        child['listMRC']      = part.listMRC
        child['productModel'] = part.productModel
        child['attrVal1']     = part.attrVal1
        child['attrVal2']     = part.attrVal2
        child['attrVal3']     = part.attrVal3
        child['attrVal4']     = part.attrVal4
        child['attrVal5']     = part.attrVal5
        arrParts.append(child)

    arrRet = {'Parts':arrParts}
    return arrRet

# Query for 1 specific model #
##############################
def queryModel(model):
    model = MODEL.query.filter_by(varName=model).first()

    retDict = {}
    retDict['varName']    = model.varName
    retDict['label']      = model.label
    retDict['family']     = model.family
    retDict['attrSet']    = model.attrSet
    retDict['isActive']   = model.isActive
    retDict['configType'] = model.configType

    return retDict