import React, {useState, useEffect} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, FlatList} from 'react-native';
import AntDesign from 'react-native-vector-icons/AntDesign';
import {useNavigation} from '@react-navigation/native';

const BudgetDetail = ({route}) => {
  const budget = route.params.budget;
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={styles.backButton}
        onPress={() => navigation.goBack()}>
        <AntDesign name="arrowleft" size={24} color="white" />
      </TouchableOpacity>
      <Text style={styles.text}>{budget.name}</Text>
      <Text style={styles.text}>Used: {budget.amount * budget.progress} </Text>
      <Text style={styles.text}>
        Used Percentage: {Math.round(budget.progress * 100)}%
      </Text>
      <Text style={styles.text}>
        Remaining: {budget.amount - budget.amount * budget.progress}{' '}
      </Text>
      <Text style={styles.text}>
        Remaining Percentage: {Math.round((1 - budget.progress) * 100)}%
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1e1e1e',
  },
  text: {
    fontSize: 20,
    fontWeight: 'bold',
    color: 'white',
  },
  backButton: {
    position: 'absolute',
    top: 12,
    left: 12,
    zIndex: 1,
  },
});

export default BudgetDetail;
