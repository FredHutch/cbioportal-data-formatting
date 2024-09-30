def get_file_metadata(table, ftype):
    tbl_fh = open(table)
    head = next(tbl_fh)
    header = head.rstrip("\n").split("\t")
    cp_idx = header.index("Cbio_project")
    ft_idx = header.index("File_Type")
    fn_idx = header.index("File_Name")
    ct_idx = header.index("Cbio_Tumor_Name")
    cn_idx = header.index("Cbio_Matched_Normal_Name")
    kt_idx = header.index("T_CL_BS_ID")
    kn_idx = header.index("Norm_BS_ID")
    meta_dict = {}
    for line in tbl_fh:
        info = line.rstrip("\n").split("\t")
        if info[ft_idx] == ftype:
            project = info[cp_idx]
            fname = info[fn_idx]
            cbio_tum_samp = info[ct_idx]
            cbio_norm_samp = info[cn_idx]
            kf_tum_samp = info[kt_idx]
            kf_norm_samp = info[kn_idx]
            if project not in meta_dict:
                meta_dict[project] = {}
            meta_dict[project][cbio_tum_samp] = {}
            meta_dict[project][cbio_tum_samp]["fname"] = fname
            meta_dict[project][cbio_tum_samp]["cbio_norm_id"] = cbio_norm_samp
            meta_dict[project][cbio_tum_samp]["kf_tum_id"] = kf_tum_samp
            meta_dict[project][cbio_tum_samp]["kf_norm_id"] = kf_norm_samp
    tbl_fh.close()
    return meta_dict
