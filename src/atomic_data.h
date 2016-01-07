/// \/file atomic_nuclear_data.h
/// \/author Andrew Davis (andrew.davis@wisc.edu)
///
/// \/brief Impliments all the fundamental atomic & nuclear data data
#include <map>

namespace pyne
{
  /// main function to be called when you whish to load the nuclide data 
  /// into memory 
  void _load_atomic_mass_map_memory();
  /// function to create mapping from nuclides in id form
  /// to their atomic masses
  void _insert_atomic_mass_map();
  /// function to create mapping from nuclides in id form 
  /// to their natural abundances
  void _insert_abund_map();
  /// Mapping from nuclides in id form to their natural abundances
  extern std::map<int,double> natural_abund_map;
  
  /// Mapping from nuclides in id form to their atomic masses.
  extern std::map<int,double> atomic_mass_map;
  
  extern std::map<int,double> atomic_mass_error_map;
} // namespace pyne
