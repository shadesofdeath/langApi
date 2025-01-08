const { SERVER_FOD_KEYWORDS } = require('./config');

// Filter Windows files based on criteria
exports.filterWindowsFiles = (file, language, hideServerFODs = false) => {
  // Check if it's a valid file type
  if (!isValidFileType(file.name, language)) {
    return false;
  }

  // Check for server FODs if needed
  if (hideServerFODs && isServerFOD(file.name, language)) {
    return false;
  }

  // Filter out specific ESD files
  if (file.name.match(/core_.*\.esd$/) ||
      file.name.match(/professional_.*\.esd$/) ||
      file.name.match(/coren_.*\.esd$/) ||
      file.name.match(/professionaln_.*\.esd$/) ||
      file.name.match(/PPIPro_.*\.esd$/) ||
      file.name.match(/ServerDatacenter_.*\.esd$/) ||
      file.name.match(/ServerStandard_.*\.esd$/) ||
      file.name.match(/ServerTurbine_.*\.esd$/)) {
    return false;
  }

  return true;
};

function isValidFileType(fileName, language) {
  return (fileName.match(/\.(esd|cab)$/) && fileName.includes(language)) ||
         fileName.match(/LanguageExperiencePack_.*\.appx$/);
}

function isServerFOD(fileName, language) {
  const locale = language.replace(/-$/, '');
  return SERVER_FOD_KEYWORDS.some(keyword => 
    fileName.match(new RegExp(escapeRegExp(keyword) + `.*${locale}\\.cab$`))
  );
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}