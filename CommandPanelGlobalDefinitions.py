"""Command panel - global definitions."""


import CommandPanel as cp


GlobalFileCmd = [
    "Std_New",
    "Std_Open",
    "Std_Save",
    "Std_Print",
    "Std_Cut",
    "Std_Copy",
    "Std_Paste",
    "Std_Undo",
    "Std_Redo",
    "Std_Refresh",
    "Std_WhatsThis"]


GlobalFile = {
    "workbench": "GlobalPanel",
    "uuid": "GlobalFile",
    "name": "File",
    "commands": GlobalFileCmd}


GlobalViewCmd = [
    "Std_ViewFitAll",
    "Std_ViewFitSelection",
    "Std_ViewIsometric",
    "Std_ViewAxo",
    "Std_ViewFront",
    "Std_ViewTop",
    "Std_ViewRight",
    "Std_ViewRear",
    "Std_ViewBottom",
    "Std_ViewLeft",
    "Std_MeasureDistance"]


GlobalView = {
    "workbench": "GlobalPanel",
    "uuid": "GlobalView",
    "name": "View",
    "commands": GlobalViewCmd}


GlobalMacroCmd = [
    "Std_DlgMacroRecord",
    "Std_MacroStopRecord",
    "Std_DlgMacroExecute",
    "Std_DlgMacroExecuteDirect"]


GlobalMacro = {
    "workbench": "GlobalPanel",
    "uuid": "GlobalMacro",
    "name": "Macro",
    "commands": GlobalMacroCmd}


GlobalDrawStyleCmd = [
    "Std_DrawStyleAsIs",
    "Std_DrawStyleFlatLines",
    "Std_DrawStyleShaded",
    "Std_DrawStyleWireframe",
    "Std_DrawStylePoints",
    "Std_DrawStyleHiddenLine",
    "Std_DrawStyleNoShading"]


GlobalDrawStyle = {
    "workbench": "GlobalPanel",
    "uuid": "GlobalDrawStyle",
    "name": "Draw style",
    "commands": GlobalDrawStyleCmd}


GlobalStructureCmd = [
    "Std_Part",
    "Std_Group"]


GlobalStructure = {
    "workbench": "GlobalPanel",
    "uuid": "GlobalStructure",
    "name": "Structure",
    "commands": GlobalStructureCmd}


GlobalFileDomain = cp.addMenu(GlobalFile)
GlobalViewDomain = cp.addMenu(GlobalView)
GlobalDrawStyleDomain = cp.addMenu(GlobalDrawStyle)
GlobalMacroDomain = cp.addMenu(GlobalMacro)
GlobalStructureDomain = cp.addMenu(GlobalStructure)


GlobalDefaultCmd = [
    GlobalFileDomain,
    GlobalViewDomain,
    GlobalDrawStyleDomain,
    GlobalMacroDomain,
    GlobalStructureDomain]


GlobalDefault = {
    "workbench": "GlobalPanel",
    "uuid": "GlobalDefault",
    "name": "Default",
    "commands": GlobalDefaultCmd,
    "default": True}


cp.addMenu(GlobalDefault)
