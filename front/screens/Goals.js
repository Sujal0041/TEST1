import React, {useState, useEffect} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, FlatList} from 'react-native';
import AntDesign from 'react-native-vector-icons/AntDesign';
import {useNavigation, useFocusEffect} from '@react-navigation/native';
import AddGoal from '../MoreScreen/AddGoals';
import {getGoalList, getGoalProgress} from '../api/api';
import {useAuth} from '../api/authContext';
import * as Progress from 'react-native-progress';

const Goals = () => {
  const navigation = useNavigation();
  const [modalVisible, setModalVisible] = useState(false);
  const [goals, setGoals] = useState([]);
  const [progressData, setProgressData] = useState([]);
  const {userToken} = useAuth();

  useFocusEffect(
    React.useCallback(() => {
      fetchGoals();
    }, []),
  );

  const fetchGoals = async () => {
    try {
      const goalsData = await getGoalList(userToken);

      setGoals(goalsData);

      const progressPromises = goalsData.map(goal =>
        getGoalProgress(userToken, goal.id),
      );
      const progressResults = await Promise.all(progressPromises);
      setProgressData(progressResults);
    } catch (error) {
      console.error(error);
    }
  };

  const renderItem = ({item, index}) => {
    const progress = progressData[index]?.progress || 0;

    let progressBarColor;
    if (progress >= 0.75) {
      progressBarColor = 'green';
    } else if (progress >= 0.3) {
      progressBarColor = 'yellow';
    } else {
      progressBarColor = 'red';
    }

    return (
      <View style={styles.goalItem}>
        <TouchableOpacity
          onPress={() =>
            navigation.navigate('GoalDetail', {
              goal: item,
              goalNumber: index + 1,
              progress,
            })
          }>
          <View style={styles.topContainer}>
            <Text style={styles.goalName}>{item.name}</Text>
          </View>
          <View style={styles.progressBar}>
            <Progress.Bar
              progress={progress}
              width={330}
              color={progressBarColor}
            />
          </View>
        </TouchableOpacity>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Goals</Text>
      <TouchableOpacity
        style={styles.plusButton}
        onPress={() => setModalVisible(true)}>
        <AntDesign name="plus" size={24} color="white" />
      </TouchableOpacity>
      <AddGoal
        modalVisible={modalVisible}
        setModalVisible={setModalVisible}
        fetchGoals={fetchGoals}
      />
      <FlatList
        data={goals}
        renderItem={renderItem}
        keyExtractor={(item, index) => index.toString()}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1e1e1e',
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 60,
  },
  text: {
    fontSize: 25,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    position: 'relative',
    bottom: 42,
  },
  goalName: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'left',
  },
  goalItem: {
    backgroundColor: '#333136',
    marginVertical: 10,
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  progressBar: {
    paddingBottom: 10,
  },
  plusButton: {
    position: 'absolute',
    top: 10,
    right: 10,
    padding: 10,
    borderRadius: 50,
    width: 60,
    alignItems: 'center',
  },
  topContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    alignItems: 'center',
  },
});

export default Goals;
