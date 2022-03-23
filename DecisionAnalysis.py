# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-03-22 22:39:17
"""
import arcpy

def DecisionAnalysis():  # DecisionAnalysis

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("3D")

    # Model Environment settings
    with arcpy.EnvManager(cellSize="10", extent="284201.4382 5033066.0794 304493.5567 5052882.3408", mask="Landuse_CSDM", 
                          scratchWorkspace=r"H:\Geog463\Demo_DecisionAnalysis_Pro\DecisionAnalysis.gdb", workspace=r"H:\Geog463\Demo_DecisionAnalysis_Pro\DecisionAnalysis.gdb"):
        HighSchools_CSDM = "HighSchools_CSDM"
        Landuse_CSDM = "Landuse_CSDM"
        DecisionAnalysis_gdb = "H:\\Geog463\\Demo_DecisionAnalysis_Pro\\DecisionAnalysis.gdb"

        # Process: Project (Project) (management)
        HighSchools_CSDM_MTM8 = "H:\\Geog463\\Demo_DecisionAnalysis_Pro\\DecisionAnalysis.gdb\\HighSchools_CSDM_MTM8"
        arcpy.management.Project(in_dataset=HighSchools_CSDM, out_dataset=HighSchools_CSDM_MTM8, out_coor_system="PROJCS[\"NAD_1983_MTM_8\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",304800.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",-73.5],PARAMETER[\"Scale_Factor\",0.9999],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", transform_method=["WGS_1984_(ITRF00)_To_NAD_1983"], in_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")

        # Process: Euclidean Distance (Euclidean Distance) (sa)
        EucDist_HS = "H:\\Geog463\\Demo_DecisionAnalysis_Pro\\DecisionAnalysis.gdb\\EucDist_HS"
        Euclidean_Distance = EucDist_HS
        Output_direction_raster = ""
        Out_back_direction_raster = ""
        with arcpy.EnvManager(scratchWorkspace=r"H:\Geog463\Demo_DecisionAnalysis_Pro\DecisionAnalysis.gdb", workspace=r"H:\Geog463\Demo_DecisionAnalysis_Pro\DecisionAnalysis.gdb"):
            EucDist_HS = arcpy.sa.EucDistance(in_source_data=HighSchools_CSDM_MTM8, maximum_distance=None, cell_size="10", out_direction_raster=Output_direction_raster, distance_method="PLANAR", in_barrier_data="", out_back_direction_raster=Out_back_direction_raster)
            EucDist_HS.save(Euclidean_Distance)


        # Process: Feature Class To Feature Class (Feature Class To Feature Class) (conversion)
        with arcpy.EnvManager(scratchWorkspace=r"H:\Geog463\Demo_DecisionAnalysis_Pro\DecisionAnalysis.gdb", workspace=r"H:\Geog463\Demo_DecisionAnalysis_Pro\DecisionAnalysis.gdb"):
            LU_Rec = arcpy.conversion.FeatureClassToFeatureClass(in_features=Landuse_CSDM, out_path=DecisionAnalysis_gdb, out_name="LU_Rec", where_clause="CATEGORY = 'Parks and Recreational'", field_mapping="CATEGORY \"CATEGORY\" true true false 40 Text 0 0,First,#,Landuse_CSDM,CATEGORY,0,40;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,Landuse_CSDM,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,Landuse_CSDM,Shape_Area,-1,-1", config_keyword="")[0]

        # Process: Euclidean Distance (2) (Euclidean Distance) (sa)
        EucDist_Rec = "H:\\Geog463\\Demo_DecisionAnalysis_Pro\\DecisionAnalysis.gdb\\EucDist_Rec"
        Euclidean_Distance_2_ = EucDist_Rec
        Output_direction_raster_2_ = ""
        Out_back_direction_raster_2_ = ""
        EucDist_Rec = arcpy.sa.EucDistance(in_source_data=LU_Rec, maximum_distance=None, cell_size="10", out_direction_raster=Output_direction_raster_2_, distance_method="PLANAR", in_barrier_data="", out_back_direction_raster=Out_back_direction_raster_2_)
        EucDist_Rec.save(Euclidean_Distance_2_)


        # Process: Reclassify (Reclassify) (sa)
        Reclass_HS = "H:\\Geog463\\Demo_DecisionAnalysis_Pro\\DecisionAnalysis.gdb\\Reclass_HS"
        Reclassify = Reclass_HS
        Reclass_HS = arcpy.sa.Reclassify(in_raster=EucDist_HS, reclass_field="VALUE", remap="0 700 0;700 1500 5;1500 999999 10", missing_values="DATA")
        Reclass_HS.save(Reclassify)


        # Process: Reclassify (2) (Reclassify) (sa)
        Reclass_Rec = "H:\\Geog463\\Demo_DecisionAnalysis_Pro\\DecisionAnalysis.gdb\\Reclass_Rec"
        Reclassify_2_ = Reclass_Rec
        Reclass_Rec = arcpy.sa.Reclassify(in_raster=EucDist_Rec, reclass_field="VALUE", remap="0 200 10;200 600 5;600 99999 0", missing_values="DATA")
        Reclass_Rec.save(Reclassify_2_)


        # Process: Weighted Overlay (Weighted Overlay) (sa)
        SuitableSites = "H:\\Geog463\\Demo_DecisionAnalysis_Pro\\DecisionAnalysis.gdb\\SuitableSites"
        Weighted_Overlay = SuitableSites
        SuitableSites = arcpy.sa.WeightedOverlay(in_weighted_overlay_table=[[Reclass_HS, 0.5, "Value", "0 1;5 2;10 3", ""], [Reclass_Rec, 0.5, "Value", "0 3;5 2;10 1", ""]])
        SuitableSites.save(Weighted_Overlay)


if __name__ == '__main__':
    DecisionAnalysis()
