CREATE DATABASE IF NOT EXISTS gestion_dpi;
CREATE TABLE IF NOT EXISTS `Staff` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nom` varchar(100),
  `prenom` varchar(100),
  `telephone` varchar(20),
  `email` varchar(100) UNIQUE,
  `adresse` varchar(255),
  `date_naissance` date,
  `mot_de_passe` varchar(255),
  `role` varchar(50)
);

CREATE TABLE IF NOT EXISTS `Patient` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nss` varchar(15) UNIQUE,
  `nom` varchar(100),
  `prenom` varchar(100),
  `date_naissance` date,
  `adresse` varchar(255),
  `telephone` varchar(20),
  `mutuelle` varchar(100),
 
  `medecin_traitant_id` int,
  `personne_a_contacter` varchar(100),
  `telephone_contact` varchar(20)
);

CREATE TABLE IF NOT EXISTS `Dossier_Patient` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `patient_id` int,
  `code_qr` varchar(255),
  `etat` varchar(20),
  `antécédents` text
);

CREATE TABLE IF NOT EXISTS `Consultation` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `dossier_patient_id` int,
  `date_consultation` datetime,
  `bilan_prescrit` text,
  `resume` text
);

CREATE TABLE IF NOT EXISTS `Soins` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `dossier_patient_id` int,
  `infirmier_id` int,
  `observation_etat_patient` text,
  `medicament_pris` boolean DEFAULT false,
  `description_soins` text,
  `date_soin` datetime
);

CREATE TABLE IF NOT EXISTS `Ordonnance` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `dossier_patient_id` int,
  `consultation_id` int,
  `medicament` text,
  `quantite` int,
  `durée` varchar(255)
);

CREATE TABLE IF NOT EXISTS `Bilan_Biologique` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `dossier_patient_id` int,
  `laborantin_id` int,
  `resultat_analyse` text,
  `resultat_examen_imagerie` text,
  `date_examen` datetime,
  `graphe` blob
);

CREATE TABLE IF NOT EXISTS `Bilan_Radiologique` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `dossier_patient_id` int,
  `radiologue_id` int,
  `compte_rendu` text,
  `images` blob,
  `date_examen` datetime
);

-- Add foreign keys after table creation
ALTER TABLE `Patient` ADD FOREIGN KEY (`medecin_traitant_id`) REFERENCES `Staff` (`id`);
ALTER TABLE `Dossier_Patient` ADD FOREIGN KEY (`patient_id`) REFERENCES `Patient` (`id`);
ALTER TABLE `Consultation` ADD FOREIGN KEY (`dossier_patient_id`) REFERENCES `Dossier_Patient` (`id`);
ALTER TABLE `Soins` ADD FOREIGN KEY (`dossier_patient_id`) REFERENCES `Dossier_Patient` (`id`);
ALTER TABLE `Soins` ADD FOREIGN KEY (`infirmier_id`) REFERENCES `Staff` (`id`);
ALTER TABLE `Ordonnance` ADD FOREIGN KEY (`dossier_patient_id`) REFERENCES `Dossier_Patient` (`id`);
ALTER TABLE `Ordonnance` ADD FOREIGN KEY (`consultation_id`) REFERENCES `Consultation` (`id`);
ALTER TABLE `Bilan_Biologique` ADD FOREIGN KEY (`dossier_patient_id`) REFERENCES `Dossier_Patient` (`id`);
ALTER TABLE `Bilan_Biologique` ADD FOREIGN KEY (`laborantin_id`) REFERENCES `Staff` (`id`);
ALTER TABLE `Bilan_Radiologique` ADD FOREIGN KEY (`dossier_patient_id`) REFERENCES `Dossier_Patient` (`id`);
ALTER TABLE `Bilan_Radiologique` ADD FOREIGN KEY (`radiologue_id`) REFERENCES `Staff` (`id`);
DESCRIBE Ordonnance;
DESCRIBE Consultation;


-- Insert some data into Staff table
-- INSERT INTO Staff (`nom`, `prenom`, `telephone`, `email`, `adresse`, `date_naissance`, `mot_de_passe`, `role`)
-- VALUES 
-- ('Admin2', 'Algiers', '0123456789', 'esi@example.com', '789 Rue Principale, Ville', '1995-03-03', 'adminadmin', 'admin');

-- Verify the data in the Staff table
SHOW COLUMNS FROM igl_app_patient;
SELECT * FROM Staff WHERE id = 35;
SHOW CREATE TABLE Patient;
-- ALTER TABLE Patient ADD CONSTRAINT FK_MedecinTraitant FOREIGN KEY (medecin_traitant_id) REFERENCES Staff(id);


SHOW COLUMNS FROM igl_app_staff;
SHOW TABLES LIKE 'igl_app_staff';

DESCRIBE igl_app_staff;
SELECT * FROM patient WHERE medecin_traitant_id NOT IN (SELECT id FROM Staff);
ALTER TABLE `Patient`
ADD COLUMN `mot_de_passe` varchar(255);

SELECT * FROM Staff;
SELECT * FROM IGL_App_staff;

SELECT * FROM Dossier_patient;
SELECT * FROM Patient;
SELECT id, nom, prenom, role FROM Staff WHERE role = 'medecin';
SHOW CREATE TABLE IGL_App_patient;
SELECT * FROM IGL_App_patient;
SHOW CREATE TABLE IGL_App_staff;
SELECT * FROM IGL_App_staff WHERE id = 35;



SELECT * FROM Dossier_patient;
SELECT * FROM Staff WHERE id =35;
UPDATE `Patient`
SET `mot_de_passe` = 'patient'  -- Replace with the actual hashed password
WHERE `id` = 13;
-- DELETE FROM Staff WHERE email = 'admin@example.com';

-- USE gestion_dpi;