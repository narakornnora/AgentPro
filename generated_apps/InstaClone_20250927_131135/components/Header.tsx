import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const Header = () => {
    return (
        <View style={styles.headerContainer}>
            <Text style={styles.headerText}>InstaClone</Text>
        </View>
    );
};

const styles = StyleSheet.create({
    headerContainer: {
        height: 60,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#ffffff',
        borderBottomWidth: 1,
        borderBottomColor: '#cccccc',
    },
    headerText: {
        fontSize: 20,
        fontWeight: 'bold',
    },
});

export default Header;