import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const Header = () => {
    return (
        <View style={styles.header}> 
            <Text style={styles.headerText}>ร้านกาแฟ</Text>
        </View>
    );
};

const styles = StyleSheet.create({
    header: {
        padding: 20,
        backgroundColor: '#6f4c3e',
    },
    headerText: {
        color: '#fff',
        fontSize: 24,
        textAlign: 'center',
    },
});

export default Header;