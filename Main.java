package com.company;

import java.util.*;

public class Main {

    public static void main(String[] args) {
	    Map<Integer, int[]> graph = new HashMap<>();
	    graph.put(0, new int[] {});
        graph.put(1, new int[] {3});
        graph.put(2, new int[] {4});
        graph.put(3, new int[] {2});
        graph.put(4, new int[] {0});
        System.out.println(traverseGraph(graph, 1));

//        System.out.println(shortestPath(graph, ));
    }

    public static boolean traverseGraph(Map<Integer, int[]> graph, int src) {
        return traverseGraph(graph, src, new HashSet<>());



    }

    public static int shortestPath(Map<Integer, int[]> graph, int src, int dest) {
        Set<Integer> traversedKeys = new HashSet<>();
        traversedKeys.add(src);

        Deque<int[]> queue = new ArrayDeque<>();
        queue.addLast(new int[] { src, 0 });

        while (queue.size() > 0) {
            int[] currentNodeInfo = queue.removeFirst();
            int currentNode = currentNodeInfo[0];
            int nodeDistance = currentNodeInfo[1];

            if (currentNode == dest) {
                return nodeDistance;
            }

            for (int neighbor : graph.get(currentNode)) {
                if (!traversedKeys.contains(neighbor)) {
                    traversedKeys.add(neighbor);
                    queue.addLast(new int[]{neighbor, nodeDistance + 1});
                }
            }
        }

        return -1;
    }

    public static boolean traverseGraph(Map<Integer, int[]> graph, int src, Set<Integer> traversedKeys) {
        if (!traversedKeys.contains(src)) {

            traversedKeys.add(src);

            for (int neighbor : graph.get(src)) {
                traverseGraph(graph, neighbor, traversedKeys);
            }
        }

        return traversedKeys.containsAll(graph.keySet());
    }
}
