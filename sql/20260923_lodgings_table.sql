CREATE TABLE `lodgings` (
    `lodging_id` CHAR(36) NOT NULL,

    `code` CHAR(32) NOT NULL,
    `name` VARCHAR(128) NOT NULL,
    `type` ENUM(
        'apartment',
        'studio',
        'house',
        'room'
    ) NOT NULL,

    `description` TEXT NULL,

    `image` VARCHAR(1024) NOT NULL DEFAULT '',

    `bedrooms` INT NOT NULL DEFAULT 0,
    `beds` INT NOT NULL DEFAULT 0,
    `bathrooms` DECIMAL(4,1) NOT NULL DEFAULT 0,
    `max_occupancy` INT NOT NULL DEFAULT 1,

    `price_per_night` DECIMAL(12,2) NOT NULL DEFAULT 0,
    `currency` CHAR(4) NOT NULL DEFAULT 'mxn',

    `check_in_time` TIME NULL,
    `check_out_time` TIME NULL,

    `address_street` VARCHAR(128) NOT NULL DEFAULT '',
    `address_external_number` VARCHAR(32) NOT NULL DEFAULT '',
    `address_internal_number` VARCHAR(32) NOT NULL DEFAULT '',
    `neighborhood` VARCHAR(128) NOT NULL DEFAULT '',

    `state_id` CHAR(2) NOT NULL DEFAULT '',
    `municipality_id` CHAR(3) NOT NULL DEFAULT '',
    `locality_id` CHAR(4) NOT NULL DEFAULT '',

    `zip` CHAR(5) NOT NULL DEFAULT '',

    `observations` TEXT NULL,

    `status` ENUM(
        'active',
        'inactive'
    ) NOT NULL DEFAULT 'active',

    `created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`lodging_id`),

    FOREIGN KEY (
        `state_id`,
        `municipality_id`,
        `locality_id`
    )
    REFERENCES `localities` (
        `state_id`,
        `municipality_id`,
        `locality_id`
    ),

    UNIQUE KEY `uk_lodgings_code` (`code`),
    UNIQUE KEY `uk_lodgings_name` (`name`),

    KEY `idx_lodgings_type` (`type`),
    KEY `idx_lodgings_status` (`status`),
    KEY `idx_lodgings_max_occupancy` (`max_occupancy`),
    KEY `idx_lodgings_price_per_night` (`price_per_night`)

);

CREATE TABLE `lodgings_amenities` (
    `amenity_id` CHAR(36) NOT NULL,
    `code` CHAR(32) NOT NULL,
    `name` VARCHAR(128) NOT NULL,
    `description` VARCHAR(255) NOT NULL DEFAULT '',
    `status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    `created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`amenity_id`),
    UNIQUE KEY (`code`)
);

CREATE TABLE `lodgings_amenities_assignments` (
    `lodging_id` CHAR(36) NOT NULL,
    `amenity_id` CHAR(36) NOT NULL,

    `created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',

    PRIMARY KEY (
        `lodging_id`,
        `amenity_id`
    ),

    FOREIGN KEY (`lodging_id`)
        REFERENCES `lodgings` (`lodging_id`),

    FOREIGN KEY (`amenity_id`)
        REFERENCES `lodgings_amenities` (`amenity_id`)
);

CREATE TABLE `lodgings_reservations` (
    `reservation_id` CHAR(36) NOT NULL,
    `lodging_id` CHAR(36) NOT NULL,

    `code` CHAR(32) NOT NULL,

    `guest_name` VARCHAR(128) NOT NULL DEFAULT '',
    `guest_email` VARCHAR(128) NOT NULL DEFAULT '',
    `guest_phone` VARCHAR(32) NOT NULL DEFAULT '',

    `check_in` DATE NOT NULL,
    `check_out` DATE NOT NULL,

    `adults` INT UNSIGNED NOT NULL DEFAULT 1,
    `children` INT UNSIGNED NOT NULL DEFAULT 0,
    `guests` INT UNSIGNED NOT NULL DEFAULT 1,

    `nights` INT UNSIGNED NOT NULL DEFAULT 1,

    `currency` CHAR(4) NOT NULL DEFAULT 'mxn',

    `observations` TEXT NULL,

    `status` ENUM(
        'confirmed',
        'cancelled',
        'completed'
    ) NOT NULL DEFAULT 'confirmed',

    `created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`reservation_id`),

    UNIQUE KEY `uk_lodgings_reservations_code` (`code`),

    KEY `idx_lodgings_reservations_lodging`
        (`lodging_id`),

    KEY `idx_lodgings_reservations_dates`
        (`lodging_id`, `check_in`, `check_out`),

    KEY `idx_lodgings_reservations_status`
        (`status`),

    CONSTRAINT `fk_lodgings_reservations_lodging`
        FOREIGN KEY (`lodging_id`)
        REFERENCES `lodgings` (`lodging_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `lodgings_reservations_charges` (
    `charge_id` CHAR(36) NOT NULL,
    `reservation_id` CHAR(36) NOT NULL,

    `type` VARCHAR(32) NOT NULL DEFAULT '',

    `name` VARCHAR(128) NOT NULL DEFAULT '',
    `description` VARCHAR(255) NOT NULL DEFAULT '',

    `quantity` DECIMAL(10,2) NOT NULL DEFAULT 1.00,
    `unit_price` DECIMAL(12,2) NOT NULL DEFAULT 0.00,

    `subtotal` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `taxes` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `total` DECIMAL(12,2) NOT NULL DEFAULT 0.00,

    `currency` CHAR(4) NOT NULL DEFAULT 'mxn',

    `status` ENUM(
        'active',
        'inactive'
    ) NOT NULL DEFAULT 'active',

    `created_at` TIMESTAMP NOT NULL DEFAULT '1990-01-01 00:00:00',
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`charge_id`),

    KEY `idx_lodgings_reservations_charges_reservation`
        (`reservation_id`),

    CONSTRAINT `fk_lodgings_reservations_charges_reservation`
        FOREIGN KEY (`reservation_id`)
        REFERENCES `lodgings_reservations` (`reservation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `lodgings_amenities`
(
    `amenity_id`,
    `code`,
    `name`
)
VALUES
(UUID(), 'air_conditioning', 'Aire acondicionado'),
(UUID(), 'wifi', 'Internet / WiFi'),
(UUID(), 'kitchen', 'Cocina'),
(UUID(), 'tv', 'Televisión'),
(UUID(), 'washer', 'Lavadora'),
(UUID(), 'dryer', 'Secadora'),
(UUID(), 'hot_water', 'Agua caliente'),
(UUID(), 'private_bathroom', 'Baño privado'),
(UUID(), 'refrigerator', 'Refrigerador'),
(UUID(), 'microwave', 'Microondas'),
(UUID(), 'coffee_maker', 'Cafetera'),
(UUID(), 'workspace', 'Espacio de trabajo'),
(UUID(), 'pet_friendly', 'Mascotas permitidas');
