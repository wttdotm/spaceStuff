import astropy.units as u
from astropy.coordinates.sky_coordinate import SkyCoord
from astroquery.skyview import SkyView
from astropy.units import Quantity
from astroquery.gaia import Gaia
from random import randrange
import matplotlib.patches as patches

from astroquery.simbad import Simbad


import matplotlib.pyplot as plt
import numpy as np

from astroquery.gaia import Gaia
tables = Gaia.load_tables(only_names=True)
# for table in (tables):
#     print (table.get_qualified_name())


coord = SkyCoord(ra=9.077502716936976, dec=40.68274, unit=(u.degree, u.degree), frame='icrs')
width = u.Quantity(5, u.arcmin)
height = u.Quantity(5, u.arcmin)
r = Gaia.query_object_async(coordinate=coord, width=width, height=height)

r.sort('phot_g_mean_mag')
# r.sort('ref_epoch')

nameOfStar = r['DESIGNATION'][0]
starRA = r['ra'][0]
starDEC = r['dec'][0]

# r/

newCoord = SkyCoord(ra=starRA, dec=starDEC, unit=(u.degree, u.degree), frame='icrs')
r.pprint(max_lines=12, max_width=130)
print(r.colnames)
# # print(len(r))
# r.pprint(r['solution_id'])

print("solution id", r['solution_id'][0])
print("source id  ", r['source_id'][0])
print("designation", r['DESIGNATION'][0])
print("ref epoch", r['ref_epoch'][0])
print("ra", starRA)
print("ra", starDEC)
# print("ra", r['ref_epoch'][0])
# # ['dist', 'solution_id', 'DESIGNATION', 'source_id', 'random_index', 'ref_epoch', 'ra', 'ra_error', 'dec', 'dec_error', 'parallax', 'parallax_error', 'parallax_over_error', 'pmra', 'pmra_error', 'pmdec', 'pmdec_error', 'ra_dec_corr', 'ra_parallax_corr', 'ra_pmra_corr', 'ra_pmdec_corr', 'dec_parallax_corr', 'dec_pmra_corr', 'dec_pmdec_corr', 'parallax_pmra_corr', 'parallax_pmdec_corr', 'pmra_pmdec_corr', 'astrometric_n_obs_al', 'astrometric_n_obs_ac', 'astrometric_n_good_obs_al', 'astrometric_n_bad_obs_al', 'astrometric_gof_al', 'astrometric_chi2_al', 'astrometric_excess_noise', 'astrometric_excess_noise_sig', 'astrometric_params_solved', 'astrometric_primary_flag', 'astrometric_weight_al', 'astrometric_pseudo_colour', 'astrometric_pseudo_colour_error', 'mean_varpi_factor_al', 'astrometric_matched_observations', 'visibility_periods_used', 'astrometric_sigma5d_max', 'frame_rotator_object_type', 'matched_observations', 'duplicated_source', 'phot_g_n_obs', 'phot_g_mean_flux', 'phot_g_mean_flux_error', 'phot_g_mean_flux_over_error', 'phot_g_mean_mag', 'phot_bp_n_obs', 'phot_bp_mean_flux', 'phot_bp_mean_flux_error', 'phot_bp_mean_flux_over_error', 'phot_bp_mean_mag', 'phot_rp_n_obs', 'phot_rp_mean_flux', 'phot_rp_mean_flux_error', 'phot_rp_mean_flux_over_error', 'phot_rp_mean_mag', 'phot_bp_rp_excess_factor', 'phot_proc_mode', 'bp_rp', 'bp_g', 'g_rp', 'radial_velocity', 'radial_velocity_error', 'rv_nb_transits', 'rv_template_teff', 'rv_template_logg', 'rv_template_fe_h', 'phot_variable_flag', 'l', 'b', 'ecl_lon', 'ecl_lat', 'priam_flags', 'teff_val', 'teff_percentile_lower', 'teff_percentile_upper', 'a_g_val', 'a_g_percentile_lower', 'a_g_percentile_upper', 'e_bp_min_rp_val', 'e_bp_min_rp_percentile_lower', 'e_bp_min_rp_percentile_upper', 'flame_flags', 'radius_val', 'radius_percentile_lower', 'radius_percentile_upper', 'lum_val', 'lum_percentile_lower', 'lum_percentile_upper', 'datalink_url', 'epoch_photometry_url']

# # arcMin = u.arcmin(1)

images = SkyView.get_images(newCoord, survey=['DSS'], radius=u.Quantity(2, u.arcmin), grid=True, gridlabels = True, pixels=200)





# # Define the custom Simbad object
# customSimbad = Simbad()

# # Add fields to fetch
# customSimbad.add_votable_fields('bibcodelist(1850-2022)')

# # Query by identifier
# result = customSimbad.query_object(nameOfStar)

# print("References To Star Found:", result)
# print("\nOther Names of Star:")

# # Query Simbad for objects at the star's coordinates
# result_table = Simbad.query_region(newCoord, radius=10 * u.arcmin)

# # Print all identifiers for the first object in the result table
# # identifiers = Simbad.query_objectids('Polaris')
# identifiers = Simbad.query_objectids(result_table['MAIN_ID'][0])
# # print(identifiers)

# print("BEFORE FOR LOOP")
# for id in identifiers:
#     print(id[0])

# result = customSimbad.query_object(identifiers[0][0])

# print("\nReferences To Star Found:", result)
# # print(result.colnames)
# ref_count = 0
# for ref in result:
#     ref_count = ref_count + 1
#     print(ref['MAIN_ID'], ref['COO_BIBCODE'])

# ax = plt.gca()
# rect = patches.Rectangle((75,75),50,50,linewidth=1,edgecolor='r',facecolor='none')

plt.imshow(images[0][0].data, cmap='cubehelix')
plt.title(f"Name of star:\n{nameOfStar}")
plt.subplots_adjust(bottom=0.3)
# plt.figtext(0.5, 0.08, f"References to star found: {ref_count} \n asc: {starRA} desc: {starDEC}", ha="center", fontsize=12, bbox={"facecolor":"white", "alpha":0.5, "pad":5})
# ax.add_patch(rect)
# plt.annotate(0,0,f"References to star found: {result} \n asc: {starRA} desc: {starDEC}")
plt.show()
# #  \n asc: {starRA} desc: {starDEC}


# job = Gaia.launch_job("select top 100 "
#                       "solution_id,ref_epoch,ra_dec_corr,astrometric_n_obs_al, "
#                       "matched_transits,duplicated_source,phot_variable_flag "
#                       "from gaiadr3.gaia_source order by source_id",
#                       output_format='votable')

# # print(job)
# # for j of job:
# #     print(j['name'], '  |  ', j['description'])