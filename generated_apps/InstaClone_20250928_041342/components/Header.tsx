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
        backgroundColor: '#f8f8f8',
        borderBottomWidth: 1,
        borderBottomColor: '#e0e0e0'
    },
    headerText: {
        fontSize: 20,
        fontWeight: 'bold'
    }
});

export default Header;