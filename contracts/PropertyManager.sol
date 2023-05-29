// SPDX-License-Identifier: UNLICENSED

pragma solidity >=0.7.0 <0.9.0;

import "./Ownable.sol";

/**
 * @title Owner
 * @dev Property contract
 */

contract PropertyManager is Ownable {
    // Variables
    uint public propertiesForSale = 0;
    Property[] public properties;

    // Mapping
    mapping (uint => address) propertyToOwner;
    mapping (address => uint) ownerPropertiesCount;

    // Events
    event NewProperty(uint id, string title, string info, bool forSale, uint price);

    // Structs
    struct Property {
        string title;
        string info;
        bool forSale;
        uint price;
    }

    // Modifiers
    modifier onlyPropertyOwner(uint id){
        require(msg.sender == propertyToOwner[id]);
        _;
    }

    // Setters and Getters
    function changeTitle(uint id, string memory newTitle) external onlyPropertyOwner(id){
        properties[id].title = newTitle;
    }

    function changeInfo(uint id, string memory newInfo) external onlyPropertyOwner(id){
        properties[id].info = newInfo;
    }

    function changePrice(uint id, uint newPrice) external onlyPropertyOwner(id){
        properties[id].price = newPrice;
    }

    function toggleForSale(uint id) external onlyPropertyOwner(id){
        if (properties[id].forSale){
            properties[id].forSale = false;
            propertiesForSale--;
        } else {
            properties[id].forSale = true;
            propertiesForSale++;
        }
    }

    // Functions
    function createProperty(string memory title, string memory info, bool forSale, uint price) public {
        properties.push(Property(title, info, forSale, price));
        uint id = properties.length - 1;
        propertyToOwner[id] = msg.sender;
        ownerPropertiesCount[msg.sender]++;
        emit NewProperty(id, title, info, forSale, price);
        if (forSale){
            propertiesForSale++;
        }
    }

    function getForSaleProperties() public view returns (Property[] memory) {
        Property[] memory forSaleProperties = new Property[](propertiesForSale);
        uint counter = 0;
        for (uint i = 0; i < properties.length; i++){
            Property memory prop = properties[i];
            if (prop.forSale) {
                forSaleProperties[counter] = prop;
                counter++;
            }
        }
        return forSaleProperties;
    }
}